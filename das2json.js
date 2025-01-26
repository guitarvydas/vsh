import fs from 'fs/promises';
import { DOMParser } from '@xmldom/xmldom';
import path from 'path';

const Direction = {
    Down: 0,
    Across: 1,
    Up: 2,
    Through: 3
};

const CellType = {
    Rhombus: 0,
    Rect: 1,
    Ellipse: 2,
    Arrow: 3
};

const FlagValue = {
    Vertex: 0,
    Edge: 1,
    Container: 2
};

const REPLACEMENTS = [
    ['&lt;', '<'],
    ['&gt;', '>'],
    ['&amp;', '&'],
    ['&quot;', '"'],
    ['&#39;', "'"],
    ['&#039;', '\\']
];

function htmlUnescape(s) {
    let result = '';
    let remaining = s;

    while (true) {
        const start = remaining.indexOf('&');
        if (start === -1) break;

        const end = remaining.indexOf(';', start);
        if (end === -1) break;

        const substr = remaining.substring(start, end + 1);
        let found = false;

        for (const [search, replace] of REPLACEMENTS) {
            if (search === substr) {
                result += remaining.substring(0, start) + replace;
                remaining = remaining.substring(end + 1);
                found = true;
                break;
            }
        }

        if (!found) {
            result += remaining.substring(0, end + 1);
            remaining = remaining.substring(end + 1);
        }
    }

    return result + remaining;
}

class Cell {
    constructor() {
        this.mxgraphId = '';
        this.mxgraphSource = '';
        this.mxgraphTarget = '';
        this.mxgraphParent = '';
        this.value = '';
        this.id = 0;
        this.source = 0;
        this.target = 0;
        this.parent = 0;
        this.flags = new Set();
        this.type = CellType.Rect;
    }

    static fromElement(doc, elem, userObjectParent = null) {
        const cell = new Cell();

        function parseStyle(styleStr) {
            const styles = styleStr.split(';');
            for (const style of styles) {
                const [key] = style.split('=');
                switch (key) {
                    case 'ellipse': cell.type = CellType.Ellipse; break;
                    case 'rhombus': cell.type = CellType.Rhombus; break;
                    case 'container': cell.flags.add(FlagValue.Container); break;
                    case 'shape': 
                        if (style.includes('rhombus')) {
                            cell.type = CellType.Rhombus;
                        }
                        break;
                }
            }
        }

        // Process mxCell attributes
        for (let i = 0; i < elem.attributes.length; i++) {
            const attr = elem.attributes[i];
            const value = attr.value;
            switch (attr.name) {
                case 'id': cell.mxgraphId = value; break;
                case 'source': cell.mxgraphSource = value; break;
                case 'target': cell.mxgraphTarget = value; break;
                case 'parent': cell.mxgraphParent = value; break;
                case 'value': cell.value = htmlUnescape(value); break;
                case 'vertex': cell.flags.add(FlagValue.Vertex); break;
                case 'edge':
                    cell.flags.add(FlagValue.Edge);
                    cell.type = CellType.Arrow;
                    break;
                case 'style': parseStyle(value); break;
            }
        }

        if (userObjectParent) {
            for (let i = 0; i < userObjectParent.attributes.length; i++) {
                const attr = userObjectParent.attributes[i];
                const value = attr.value;
                switch (attr.name) {
                    case 'id': cell.mxgraphId = value; break;
                    case 'label': cell.value = value; break;
                }
            }
        }

        return cell;
    }
}

class Page {
    constructor() {
        this.name = '';
        this.cells = [];
    }

    static fromElement(doc, elem) {
        const page = new Page();
        
        const parent1 = elem.parentNode.parentNode;
        if (parent1.nodeName !== 'diagram') {
            throw new Error('Unexpected XML layout (root diagram name)');
        }
        page.name = parent1.getAttribute('name');
        if (!page.name) {
            throw new Error('Page without name');
        }

        const cells = [];
        for (let i = 0; i < elem.childNodes.length; i++) {
            const child = elem.childNodes[i];
            if (!child.nodeName) continue;
            
            if (child.nodeName === 'mxCell') {
                cells.push(Cell.fromElement(doc, child));
            } else if (child.nodeName === 'UserObject') {
                const mxCells = child.getElementsByTagName('mxCell');
                if (mxCells.length > 0) {
                    cells.push(Cell.fromElement(doc, mxCells[0], child));
                }
            }
        }

        page.cells = cells.sort((a, b) => a.type - b.type);
        page.cells.forEach((cell, idx) => cell.id = idx);

        for (const cell of page.cells) {
            for (const x of page.cells) {
                if (cell.mxgraphSource === x.mxgraphId) cell.source = x.id;
                if (cell.mxgraphTarget === x.mxgraphId) cell.target = x.id;
                if (cell.mxgraphParent === x.mxgraphId) cell.parent = x.id;
            }
        }

        return page;
    }
}

function collectChildren(cells) {
    return cells
        .filter(cell => cell.type === CellType.Rect && cell.flags.has(FlagValue.Container))
        .map(cell => ({ name: cell.value, id: cell.id }));
}

function collectUpDecls(cells, decls) {
    for (const cell of cells) {
        if (cell.type !== CellType.Arrow) continue;

        const decl = {
            dir: Direction.Up,
            source_port: '',
            target_port: '',
            source: null
        };

        const targetRhombus = cells[cell.target];
        if (targetRhombus.type !== CellType.Rhombus) continue;

        const sourceCell = cells[cell.source];
        decl.source_port = sourceCell.value;
        decl.target_port = targetRhombus.value;

        const parentRect = cells[sourceCell.parent];
        if (!(parentRect.type === CellType.Rect && parentRect.flags.has(FlagValue.Container))) {
            continue;
        }

        decl.source = { name: parentRect.value, id: parentRect.id };
        decls.push(decl);
    }
}

function collectAcrossDecls(cells, decls) {
    for (const cell of cells) {
        if (cell.type !== CellType.Arrow) continue;

        const decl = {
            dir: Direction.Across,
            source_port: '',
            target_port: '',
            source: null,
            target: null
        };

        const sourcePort = cells[cell.source];
        const targetPort = cells[cell.target];

        decl.source_port = sourcePort.value;
        decl.target_port = targetPort.value;

        const sourceRect = cells[sourcePort.parent];
        const targetRect = cells[targetPort.parent];

        if (!(sourceRect.type === CellType.Rect && sourceRect.flags.has(FlagValue.Container))) {
            continue;
        }
        if (!(targetRect.type === CellType.Rect && targetRect.flags.has(FlagValue.Container))) {
            continue;
        }

        decl.source = { name: sourceRect.value, id: sourceRect.id };
        decl.target = { name: targetRect.value, id: targetRect.id };
        decls.push(decl);
    }
}

function collectDownDecls(cells, decls) {
    for (const cell of cells) {
        if (cell.type !== CellType.Arrow) continue;

        const decl = {
            dir: Direction.Down,
            source_port: '',
            target_port: '',
            target: null
        };

        const sourceRhombus = cells[cell.source];
        if (sourceRhombus.type !== CellType.Rhombus) continue;

        const targetCell = cells[cell.target];
        if (targetCell.type !== CellType.Rect) continue;

        decl.source_port = sourceRhombus.value;
        decl.target_port = targetCell.value;

        const parentRect = cells[targetCell.parent];
        if (parentRect.type !== CellType.Rect || !parentRect.flags.has(FlagValue.Container)) {
            continue;
        }

        decl.target = { name: parentRect.value, id: parentRect.id };
        decls.push(decl);
    }
}

function collectThroughDecls(cells, decls) {
    for (const cell of cells) {
        if (cell.type !== CellType.Arrow) continue;

        const sourceRhombus = cells[cell.source];
        const targetRhombus = cells[cell.target];
        if (sourceRhombus.type !== CellType.Rhombus) continue;
        if (targetRhombus.type !== CellType.Rhombus) continue;

        decls.push({
            dir: Direction.Through,
            source_port: sourceRhombus.value,
            target_port: targetRhombus.value
        });
    }
}

function lintConnections(name, cells) {
    let ok = true;
    
    let drawioTopIdx = cells.find(cell => cell.parent === 0)?.id;
    let drawioSecondIdx = cells.find(cell => cell.parent === drawioTopIdx)?.id;

    for (const cell of cells) {
        if (cell.type !== CellType.Arrow) continue;

        const sourcePort = cells[cell.source];
        const targetPort = cells[cell.target];

        if ((sourcePort.type === CellType.Rhombus && sourcePort.parent === drawioTopIdx) ||
            (sourcePort.type === CellType.Rect && (sourcePort.parent === drawioTopIdx || sourcePort.parent === drawioSecondIdx)) ||
            (targetPort.type === CellType.Rhombus && targetPort.parent === drawioTopIdx) ||
            (targetPort.type === CellType.Rect && (targetPort.parent === drawioTopIdx || targetPort.parent === drawioSecondIdx))) {
            
            console.error(`suspicious (in ${name}) cell ${sourcePort.value}->${targetPort.value} in connection (port not contained by container?)`);
            ok = false;
        }
    }

    if (!ok) {
        throw new Error('quit: suspicious drawing');
    }
}

async function drawio2json(containerXml) {
    try {
        const xmlContent = await fs.readFile(containerXml, 'utf8');
        const parser = new DOMParser();
        const doc = parser.parseFromString(xmlContent, 'text/xml');
        
        if (!doc) {
            throw new Error('Failed to parse XML');
        }

        const roots = doc.getElementsByTagName('root');
        const containers = [];
        
        for (let i = 0; i < roots.length; i++) {
            const page = Page.fromElement(doc, roots[i]);
            const container = containerDeclFromPage(page);
            container.file = containerXml;
            containers.push(container);
        }

        const jsonOutput = JSON.stringify(containers, null, 2);
        const filename = path.basename(containerXml) + '.json';
        
        await fs.writeFile(filename, jsonOutput);
        return filename;
    } catch (err) {
        console.error('Error:', err);
        throw err;
    }
}

function containerDeclFromPage(page) {
    const decl = {
        name: page.name,
        children: collectChildren(page.cells),
        connections: []
    };

    lintConnections(page.name, page.cells);

    const connections = [];
    collectDownDecls(page.cells, connections);
    collectAcrossDecls(page.cells, connections);
    collectUpDecls(page.cells, connections);
    collectThroughDecls(page.cells, connections);
    decl.connections = connections;

    return decl;
}

async function parseCommandLineArgs() {
    const diagramSourceFile = process.argv[2] || '<?>';

    try {
        await fs.access(diagramSourceFile);
    } catch {
        console.error('Source diagram file', diagramSourceFile, 'does not exist.');
        process.exit(1);
    }

    return diagramSourceFile;
}

async function main() {
    const diagramName = await parseCommandLineArgs();
    try {
        const fname = await drawio2json(diagramName);
        console.log('Created:', fname);
    } catch (err) {
        console.error('Error:', err);
        process.exit(1);
    }
}

main();
