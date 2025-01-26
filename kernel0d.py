

import sys
import re
import subprocess
import shlex
import os
import json
from collections import deque
                                                            #line 1#line 2
ticktime =  0                                               #line 3
counter =  0                                                #line 4#line 5
digits = [ "₀", "₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉", "₁₀", "₁₁", "₁₂", "₁₃", "₁₄", "₁₅", "₁₆", "₁₇", "₁₈", "₁₉", "₂₀", "₂₁", "₂₂", "₂₃", "₂₄", "₂₅", "₂₆", "₂₇", "₂₈", "₂₉"]#line 12#line 13#line 14
def gensymbol (s):                                          #line 15
    global counter                                          #line 16
    name_with_id =  str( s) + subscripted_digit ( counter)  #line 17
    counter =  counter+ 1                                   #line 18
    return  name_with_id                                    #line 19#line 20#line 21

def subscripted_digit (n):                                  #line 22
    global digits                                           #line 23
    if ( n >=  0 and  n <=  29):                            #line 24
        return  digits [ n]                                 #line 25
    else:                                                   #line 26
        return  str( "₊") + str ( n)                        #line 27#line 28#line 29#line 30

class Datum:
    def __init__ (self,):                                   #line 31
        self.v =  None                                      #line 32
        self.clone =  None                                  #line 33
        self.reclaim =  None                                #line 34
        self.other =  None # reserved for use on per-project basis #line 35#line 36
                                                            #line 37
def new_datum_string (s):                                   #line 38
    d =  Datum ()                                           #line 39
    d.v =  s                                                #line 40
    d.clone =  lambda : clone_datum_string ( d)             #line 41
    d.reclaim =  lambda : reclaim_datum_string ( d)         #line 42
    return  d                                               #line 43#line 44#line 45

def clone_datum_string (d):                                 #line 46
    newd = new_datum_string ( d.v)                          #line 47
    return  newd                                            #line 48#line 49#line 50

def reclaim_datum_string (src):                             #line 51
    pass                                                    #line 52#line 53#line 54

def new_datum_bang ():                                      #line 55
    p =  Datum ()                                           #line 56
    p.v =  ""                                               #line 57
    p.clone =  lambda : clone_datum_bang ( p)               #line 58
    p.reclaim =  lambda : reclaim_datum_bang ( p)           #line 59
    return  p                                               #line 60#line 61#line 62

def clone_datum_bang (d):                                   #line 63
    return new_datum_bang ()                                #line 64#line 65#line 66

def reclaim_datum_bang (d):                                 #line 67
    pass                                                    #line 68#line 69#line 70

# Message passed to a leaf component.                       #line 71
#                                                           #line 72
# `port` refers to the name of the incoming or outgoing port of this component.#line 73
# `datum` is the data attached to this message.             #line 74
class Message:
    def __init__ (self,):                                   #line 75
        self.port =  None                                   #line 76
        self.datum =  None                                  #line 77#line 78
                                                            #line 79
def clone_port (s):                                         #line 80
    return clone_string ( s)                                #line 81#line 82#line 83

# Utility for making a `Message`. Used to safely “seed“ messages#line 84
# entering the very top of a network.                       #line 85
def make_message (port,datum):                              #line 86
    p = clone_string ( port)                                #line 87
    m =  Message ()                                         #line 88
    m.port =  p                                             #line 89
    m.datum =  datum.clone ()                               #line 90
    return  m                                               #line 91#line 92#line 93

# Clones a message. Primarily used internally for “fanning out“ a message to multiple destinations.#line 94
def message_clone (msg):                                    #line 95
    m =  Message ()                                         #line 96
    m.port = clone_port ( msg.port)                         #line 97
    m.datum =  msg.datum.clone ()                           #line 98
    return  m                                               #line 99#line 100#line 101

# Frees a message.                                          #line 102
def destroy_message (msg):                                  #line 103
    # during debug, dont destroy any message, since we want to trace messages, thus, we need to persist ancestor messages#line 104
    pass                                                    #line 105#line 106#line 107

def destroy_datum (msg):                                    #line 108
    pass                                                    #line 109#line 110#line 111

def destroy_port (msg):                                     #line 112
    pass                                                    #line 113#line 114#line 115

#                                                           #line 116
def format_message (m):                                     #line 117
    if  m ==  None:                                         #line 118
        # return  str( "‹") +  str( m.port) +  str( "›:‹") +  str( "ϕ") +  "›,"    #line 119
        return "{}"
    else:                                                   #line 120
        # return  str( "‹") +  str( m.port) +  str( "›:‹") +  str( m.datum.v) +  "›,"    #line 121#line 122#line 123#line 124
        return "{" + f'"{m.port}":"{m.datum.v}"' + "}"

enumDown =  0                                               #line 125
enumAcross =  1                                             #line 126
enumUp =  2                                                 #line 127
enumThrough =  3                                            #line 128#line 129
def create_down_connector (container,proto_conn,connectors,children_by_id):#line 130
    # JSON: {;dir': 0, 'source': {'name': '', 'id': 0}, 'source_port': '', 'target': {'name': 'Echo', 'id': 12}, 'target_port': ''},#line 131
    connector =  Connector ()                               #line 132
    connector.direction =  "down"                           #line 133
    connector.sender = mkSender ( container.name, container, proto_conn [ "source_port"])#line 134
    target_proto =  proto_conn [ "target"]                  #line 135
    id_proto =  target_proto [ "id"]                        #line 136
    target_component =  children_by_id [id_proto]           #line 137
    if ( target_component ==  None):                        #line 138
        load_error ( str( "internal error: .Down connection target internal error ") + ( proto_conn [ "target"]) [ "name"] )#line 139
    else:                                                   #line 140
        connector.receiver = mkReceiver ( target_component.name, target_component, proto_conn [ "target_port"], target_component.inq)#line 141#line 142
    return  connector                                       #line 143#line 144#line 145

def create_across_connector (container,proto_conn,connectors,children_by_id):#line 146
    connector =  Connector ()                               #line 147
    connector.direction =  "across"                         #line 148
    source_component =  children_by_id [(( proto_conn [ "source"]) [ "id"])]#line 149
    target_component =  children_by_id [(( proto_conn [ "target"]) [ "id"])]#line 150
    if  source_component ==  None:                          #line 151
        load_error ( str( "internal error: .Across connection source not ok ") + ( proto_conn [ "source"]) [ "name"] )#line 152
    else:                                                   #line 153
        connector.sender = mkSender ( source_component.name, source_component, proto_conn [ "source_port"])#line 154
        if  target_component ==  None:                      #line 155
            load_error ( str( "internal error: .Across connection target not ok ") + ( proto_conn [ "target"]) [ "name"] )#line 156
        else:                                               #line 157
            connector.receiver = mkReceiver ( target_component.name, target_component, proto_conn [ "target_port"], target_component.inq)#line 158#line 159#line 160
    return  connector                                       #line 161#line 162#line 163

def create_up_connector (container,proto_conn,connectors,children_by_id):#line 164
    connector =  Connector ()                               #line 165
    connector.direction =  "up"                             #line 166
    source_component =  children_by_id [(( proto_conn [ "source"]) [ "id"])]#line 167
    if  source_component ==  None:                          #line 168
        load_error ( str( "internal error: .Up connection source not ok ") + ( proto_conn [ "source"]) [ "name"] )#line 169
    else:                                                   #line 170
        connector.sender = mkSender ( source_component.name, source_component, proto_conn [ "source_port"])#line 171
        connector.receiver = mkReceiver ( container.name, container, proto_conn [ "target_port"], container.outq)#line 172#line 173
    return  connector                                       #line 174#line 175#line 176

def create_through_connector (container,proto_conn,connectors,children_by_id):#line 177
    connector =  Connector ()                               #line 178
    connector.direction =  "through"                        #line 179
    connector.sender = mkSender ( container.name, container, proto_conn [ "source_port"])#line 180
    connector.receiver = mkReceiver ( container.name, container, proto_conn [ "target_port"], container.outq)#line 181
    return  connector                                       #line 182#line 183#line 184
                                                            #line 185
def container_instantiator (reg,owner,container_name,desc): #line 186
    global enumDown, enumUp, enumAcross, enumThrough        #line 187
    container = make_container ( container_name, owner)     #line 188
    children = []                                           #line 189
    children_by_id = {}
    # not strictly necessary, but, we can remove 1 runtime lookup by “compiling it out“ here#line 190
    # collect children                                      #line 191
    for child_desc in  desc [ "children"]:                  #line 192
        child_instance = get_component_instance ( reg, child_desc [ "name"], container)#line 193
        children.append ( child_instance)                   #line 194
        id =  child_desc [ "id"]                            #line 195
        children_by_id [id] =  child_instance               #line 196#line 197#line 198
    container.children =  children                          #line 199#line 200
    connectors = []                                         #line 201
    for proto_conn in  desc [ "connections"]:               #line 202
        connector =  Connector ()                           #line 203
        if  proto_conn [ "dir"] ==  enumDown:               #line 204
            connectors.append (create_down_connector ( container, proto_conn, connectors, children_by_id)) #line 205
        elif  proto_conn [ "dir"] ==  enumAcross:           #line 206
            connectors.append (create_across_connector ( container, proto_conn, connectors, children_by_id)) #line 207
        elif  proto_conn [ "dir"] ==  enumUp:               #line 208
            connectors.append (create_up_connector ( container, proto_conn, connectors, children_by_id)) #line 209
        elif  proto_conn [ "dir"] ==  enumThrough:          #line 210
            connectors.append (create_through_connector ( container, proto_conn, connectors, children_by_id)) #line 211#line 212#line 213
    container.connections =  connectors                     #line 214
    return  container                                       #line 215#line 216#line 217

# The default handler for container components.             #line 218
def container_handler (container,message):                  #line 219
    route ( container, container, message)
    # references to 'self' are replaced by the container during instantiation#line 220
    while any_child_ready ( container):                     #line 221
        step_children ( container, message)                 #line 222#line 223#line 224

# Frees the given container and associated data.            #line 225
def destroy_container (eh):                                 #line 226
    pass                                                    #line 227#line 228#line 229

# Routing connection for a container component. The `direction` field has#line 230
# no affect on the default message routing system _ it is there for debugging#line 231
# purposes, or for reading by other tools.                  #line 232#line 233
class Connector:
    def __init__ (self,):                                   #line 234
        self.direction =  None # down, across, up, through  #line 235
        self.sender =  None                                 #line 236
        self.receiver =  None                               #line 237#line 238
                                                            #line 239
# `Sender` is used to “pattern match“ which `Receiver` a message should go to,#line 240
# based on component ID (pointer) and port name.            #line 241#line 242
class Sender:
    def __init__ (self,):                                   #line 243
        self.name =  None                                   #line 244
        self.component =  None                              #line 245
        self.port =  None                                   #line 246#line 247
                                                            #line 248#line 249#line 250
# `Receiver` is a handle to a destination queue, and a `port` name to assign#line 251
# to incoming messages to this queue.                       #line 252#line 253
class Receiver:
    def __init__ (self,):                                   #line 254
        self.name =  None                                   #line 255
        self.queue =  None                                  #line 256
        self.port =  None                                   #line 257
        self.component =  None                              #line 258#line 259
                                                            #line 260
def mkSender (name,component,port):                         #line 261
    s =  Sender ()                                          #line 262
    s.name =  name                                          #line 263
    s.component =  component                                #line 264
    s.port =  port                                          #line 265
    return  s                                               #line 266#line 267#line 268

def mkReceiver (name,component,port,q):                     #line 269
    r =  Receiver ()                                        #line 270
    r.name =  name                                          #line 271
    r.component =  component                                #line 272
    r.port =  port                                          #line 273
    # We need a way to determine which queue to target. "Down" and "Across" go to inq, "Up" and "Through" go to outq.#line 274
    r.queue =  q                                            #line 275
    return  r                                               #line 276#line 277#line 278

# Checks if two senders match, by pointer equality and port name matching.#line 279
def sender_eq (s1,s2):                                      #line 280
    same_components = ( s1.component ==  s2.component)      #line 281
    same_ports = ( s1.port ==  s2.port)                     #line 282
    return  same_components and  same_ports                 #line 283#line 284#line 285

# Delivers the given message to the receiver of this connector.#line 286#line 287
def deposit (parent,conn,message):                          #line 288
    new_message = make_message ( conn.receiver.port, message.datum)#line 289
    push_message ( parent, conn.receiver.component, conn.receiver.queue, new_message)#line 290#line 291#line 292

def force_tick (parent,eh):                                 #line 293
    tick_msg = make_message ( ".",new_datum_bang ())        #line 294
    push_message ( parent, eh, eh.inq, tick_msg)            #line 295
    return  tick_msg                                        #line 296#line 297#line 298

def push_message (parent,receiver,inq,m):                   #line 299
    inq.append ( m)                                         #line 300
    parent.visit_ordering.append ( receiver)                #line 301#line 302#line 303

def is_self (child,container):                              #line 304
    # in an earlier version “self“ was denoted as ϕ         #line 305
    return  child ==  container                             #line 306#line 307#line 308

def step_child (child,msg):                                 #line 309
    before_state =  child.state                             #line 310
    child.handler ( child, msg)                             #line 311
    after_state =  child.state                              #line 312
    return [ before_state ==  "idle" and  after_state!= "idle", before_state!= "idle" and  after_state!= "idle", before_state!= "idle" and  after_state ==  "idle"]#line 315#line 316#line 317

def step_children (container,causingMessage):               #line 318
    container.state =  "idle"                               #line 319
    for child in  list ( container.visit_ordering):         #line 320
        # child = container represents self, skip it        #line 321
        if (not (is_self ( child, container))):             #line 322
            if (not ((0==len( child.inq)))):                #line 323
                msg =  child.inq.popleft ()                 #line 324
                began_long_run =  None                      #line 325
                continued_long_run =  None                  #line 326
                ended_long_run =  None                      #line 327
                [ began_long_run, continued_long_run, ended_long_run] = step_child ( child, msg)#line 328
                if  began_long_run:                         #line 329
                    pass                                    #line 330
                elif  continued_long_run:                   #line 331
                    pass                                    #line 332
                elif  ended_long_run:                       #line 333
                    pass                                    #line 334#line 335
                destroy_message ( msg)                      #line 336
            else:                                           #line 337
                if  child.state!= "idle":                   #line 338
                    msg = force_tick ( container, child)    #line 339
                    child.handler ( child, msg)             #line 340
                    destroy_message ( msg)                  #line 341#line 342#line 343#line 344
            if  child.state ==  "active":                   #line 345
                # if child remains active, then the container must remain active and must propagate “ticks“ to child#line 346
                container.state =  "active"                 #line 347#line 348#line 349
            while (not ((0==len( child.outq)))):            #line 350
                msg =  child.outq.popleft ()                #line 351
                route ( container, child, msg)              #line 352
                destroy_message ( msg)                      #line 353#line 354#line 355#line 356#line 357#line 358

def attempt_tick (parent,eh):                               #line 359
    if  eh.state!= "idle":                                  #line 360
        force_tick ( parent, eh)                            #line 361#line 362#line 363#line 364

def is_tick (msg):                                          #line 365
    return  "." ==  msg.port
    # assume that any message that is sent to port "." is a tick #line 366#line 367#line 368

# Routes a single message to all matching destinations, according to#line 369
# the container's connection network.                       #line 370#line 371
def route (container,from_component,message):               #line 372
    was_sent =  False
    # for checking that output went somewhere (at least during bootstrap)#line 373
    fromname =  ""                                          #line 374
    global ticktime                                         #line 375
    ticktime ==  ticktime+ 1                                #line 376
    if is_tick ( message):                                  #line 377
        for child in  container.children:                   #line 378
            attempt_tick ( container, child)                #line 379
        was_sent =  True                                    #line 380
    else:                                                   #line 381
        if (not (is_self ( from_component, container))):    #line 382
            fromname =  from_component.name                 #line 383
        else:                                               #line 384
            fromname =  container.name                      #line 385#line 386
        from_sender = mkSender ( fromname, from_component, message.port)#line 387#line 388
        for connector in  container.connections:            #line 389
            if sender_eq ( from_sender, connector.sender):  #line 390
                deposit ( container, connector, message)    #line 391
                was_sent =  True                            #line 392#line 393#line 394#line 395
    if not ( was_sent):                                     #line 396
        print ( "\n\n*** Error: ***")                       #line 397
        print ( "***")                                      #line 398
        print ( str( container.name) +  str( ": message '") +  str( message.port) +  str( "' from ") +  str( fromname) +  " dropped on floor..."     )#line 399
        print ( "***")                                      #line 400
        exit ()                                             #line 401#line 402#line 403#line 404

def any_child_ready (container):                            #line 405
    for child in  container.children:                       #line 406
        if child_is_ready ( child):                         #line 407
            return  True                                    #line 408#line 409#line 410
    return  False                                           #line 411#line 412#line 413

def child_is_ready (eh):                                    #line 414
    return (not ((0==len( eh.outq)))) or (not ((0==len( eh.inq)))) or ( eh.state!= "idle") or (any_child_ready ( eh))#line 415#line 416#line 417

def append_routing_descriptor (container,desc):             #line 418
    container.routings.append ( desc)                       #line 419#line 420#line 421

def container_injector (container,message):                 #line 422
    container_handler ( container, message)                 #line 423#line 424#line 425
                                                            #line 426#line 427#line 428
class Component_Registry:
    def __init__ (self,):                                   #line 429
        self.templates = {}                                 #line 430#line 431
                                                            #line 432
class Template:
    def __init__ (self,):                                   #line 433
        self.name =  None                                   #line 434
        self.template_data =  None                          #line 435
        self.instantiator =  None                           #line 436#line 437
                                                            #line 438
def mkTemplate (name,template_data,instantiator):           #line 439
    templ =  Template ()                                    #line 440
    templ.name =  name                                      #line 441
    templ.template_data =  template_data                    #line 442
    templ.instantiator =  instantiator                      #line 443
    return  templ                                           #line 444#line 445#line 446

def read_and_convert_json_file (pathname,filename):         #line 447

    try:
        fil = open(filename, "r")
        json_data = fil.read()
        routings = json.loads(json_data)
        fil.close ()
        return routings
    except FileNotFoundError:
        print (f"File not found: '{filename}'")
        return None
    except json.JSONDecodeError as e:
        print ("Error decoding JSON in file: '{e}'")
        return None
                                                            #line 448#line 449#line 450

def json2internal (pathname,container_xml):                 #line 451
    fname =  os.path.basename ( container_xml)              #line 452
    routings = read_and_convert_json_file ( pathname, fname)#line 453
    return  routings                                        #line 454#line 455#line 456

def delete_decls (d):                                       #line 457
    pass                                                    #line 458#line 459#line 460

def make_component_registry ():                             #line 461
    return  Component_Registry ()                           #line 462#line 463#line 464

def register_component (reg,template):
    return abstracted_register_component ( reg, template, False)#line 465

def register_component_allow_overwriting (reg,template):
    return abstracted_register_component ( reg, template, True)#line 466#line 467

def abstracted_register_component (reg,template,ok_to_overwrite):#line 468
    name = mangle_name ( template.name)                     #line 469
    if  reg!= None and  name in  reg.templates and not  ok_to_overwrite:#line 470
        load_error ( str( "Component /") +  str( template.name) +  "/ already declared"  )#line 471
        return  reg                                         #line 472
    else:                                                   #line 473
        reg.templates [name] =  template                    #line 474
        return  reg                                         #line 475#line 476#line 477#line 478

def get_component_instance (reg,full_name,owner):           #line 479
    template_name = mangle_name ( full_name)                #line 480
    if  template_name in  reg.templates:                    #line 481
        template =  reg.templates [template_name]           #line 482
        if ( template ==  None):                            #line 483
            load_error ( str( "Registry Error (A): Can't find component /") +  str( template_name) +  "/"  )#line 484
            return  None                                    #line 485
        else:                                               #line 486
            owner_name =  ""                                #line 487
            instance_name =  template_name                  #line 488
            if  None!= owner:                               #line 489
                owner_name =  owner.name                    #line 490
                instance_name =  str( owner_name) +  str( ".") +  template_name  #line 491
            else:                                           #line 492
                instance_name =  template_name              #line 493#line 494
            instance =  template.instantiator ( reg, owner, instance_name, template.template_data)#line 495
            return  instance                                #line 496#line 497
    else:                                                   #line 498
        load_error ( str( "Registry Error (B): Can't find component /") +  str( template_name) +  "/"  )#line 499
        return  None                                        #line 500#line 501#line 502#line 503

def dump_registry (reg):                                    #line 504
    nl ()                                                   #line 505
    print ( "*** PALETTE ***")                              #line 506
    for c in  reg.templates:                                #line 507
        print ( c.name)                                     #line 508
    print ( "***************")                              #line 509
    nl ()                                                   #line 510#line 511#line 512

def print_stats (reg):                                      #line 513
    print ( str( "registry statistics: ") +  reg.stats )    #line 514#line 515#line 516

def mangle_name (s):                                        #line 517
    # trim name to remove code from Container component names _ deferred until later (or never)#line 518
    return  s                                               #line 519#line 520#line 521
                                                            #line 522
# Data for an asyncronous component _ effectively, a function with input#line 523
# and output queues of messages.                            #line 524
#                                                           #line 525
# Components can either be a user_supplied function (“lea“), or a “container“#line 526
# that routes messages to child components according to a list of connections#line 527
# that serve as a message routing table.                    #line 528
#                                                           #line 529
# Child components themselves can be leaves or other containers.#line 530
#                                                           #line 531
# `handler` invokes the code that is attached to this component.#line 532
#                                                           #line 533
# `instance_data` is a pointer to instance data that the `leaf_handler`#line 534
# function may want whenever it is invoked again.           #line 535
#                                                           #line 536#line 537
# Eh_States :: enum { idle, active }                        #line 538
class Eh:
    def __init__ (self,):                                   #line 539
        self.name =  ""                                     #line 540
        self.inq =  deque ([])                              #line 541
        self.outq =  deque ([])                             #line 542
        self.owner =  None                                  #line 543
        self.children = []                                  #line 544
        self.visit_ordering =  deque ([])                   #line 545
        self.connections = []                               #line 546
        self.routings =  deque ([])                         #line 547
        self.handler =  None                                #line 548
        self.finject =  None                                #line 549
        self.instance_data =  None                          #line 550
        self.state =  "idle"                                #line 551# bootstrap debugging#line 552
        self.kind =  None # enum { container, leaf, }       #line 553#line 554
                                                            #line 555
# Creates a component that acts as a container. It is the same as a `Eh` instance#line 556
# whose handler function is `container_handler`.            #line 557
def make_container (name,owner):                            #line 558
    eh =  Eh ()                                             #line 559
    eh.name =  name                                         #line 560
    eh.owner =  owner                                       #line 561
    eh.handler =  container_handler                         #line 562
    eh.finject =  container_injector                        #line 563
    eh.state =  "idle"                                      #line 564
    eh.kind =  "container"                                  #line 565
    return  eh                                              #line 566#line 567#line 568

# Creates a new leaf component out of a handler function, and a data parameter#line 569
# that will be passed back to your handler when called.     #line 570#line 571
def make_leaf (name,owner,instance_data,handler):           #line 572
    eh =  Eh ()                                             #line 573
    eh.name =  str( owner.name) +  str( ".") +  name        #line 574
    eh.owner =  owner                                       #line 575
    eh.handler =  handler                                   #line 576
    eh.instance_data =  instance_data                       #line 577
    eh.state =  "idle"                                      #line 578
    eh.kind =  "leaf"                                       #line 579
    return  eh                                              #line 580#line 581#line 582

# Sends a message on the given `port` with `data`, placing it on the output#line 583
# of the given component.                                   #line 584#line 585
def send (eh,port,datum,causingMessage):                    #line 586
    msg = make_message ( port, datum)                       #line 587
    put_output ( eh, msg)                                   #line 588#line 589#line 590

def send_string (eh,port,s,causingMessage):                 #line 591
    datum = new_datum_string ( s)                           #line 592
    msg = make_message ( port, datum)                       #line 593
    put_output ( eh, msg)                                   #line 594#line 595#line 596

def forward (eh,port,msg):                                  #line 597
    fwdmsg = make_message ( port, msg.datum)                #line 598
    put_output ( eh, fwdmsg)                                #line 599#line 600#line 601

def inject (eh,msg):                                        #line 602
    eh.finject ( eh, msg)                                   #line 603#line 604#line 605

# Returns a list of all output messages on a container.     #line 606
# For testing / debugging purposes.                         #line 607#line 608
def output_list (eh):                                       #line 609
    return  eh.outq                                         #line 610#line 611#line 612

# Utility for printing an array of messages.                #line 613
def print_output_list (eh):                                 #line 614
    i = len (eh.outq)
    for m in  list ( eh.outq):                              #line 616
        print (format_message ( m))                         #line 617#line 618
        i -= 1
        if i > 0:
            print ( ",")                                            #line 619#line 620#line 621

def spaces (n):                                             #line 622
    s =  ""                                                 #line 623
    for i in range( n):                                     #line 624
        s =  s+ " "                                         #line 625
    return  s                                               #line 626#line 627#line 628

def set_active (eh):                                        #line 629
    eh.state =  "active"                                    #line 630#line 631#line 632

def set_idle (eh):                                          #line 633
    eh.state =  "idle"                                      #line 634#line 635#line 636

# Utility for printing a specific output message.           #line 637#line 638
def fetch_first_output (eh,port):                           #line 639
    for msg in  list ( eh.outq):                            #line 640
        if ( msg.port ==  port):                            #line 641
            return  msg.datum                               #line 642
    return  None                                            #line 643#line 644#line 645

def print_specific_output (eh,port):                        #line 646
    # port ∷ “”                                             #line 647
    datum = fetch_first_output ( eh, port)                  #line 648
    print ( datum.v)                                        #line 649#line 650

def print_specific_output_to_stderr (eh,port):              #line 651
    # port ∷ “”                                             #line 652
    datum = fetch_first_output ( eh, port)                  #line 653
    # I don't remember why I found it useful to print to stderr during bootstrapping, so I've left it in...#line 654
    print ( datum.v, file=sys.stderr)                       #line 655#line 656#line 657

def put_output (eh,msg):                                    #line 658
    eh.outq.append ( msg)                                   #line 659#line 660#line 661

root_project =  ""                                          #line 662
root_0D =  ""                                               #line 663#line 664
def set_environment (rproject,r0D):                         #line 665
    global root_project                                     #line 666
    global root_0D                                          #line 667
    root_project =  rproject                                #line 668
    root_0D =  r0D                                          #line 669#line 670#line 671
                                                            #line 672
def string_make_persistent (s):                             #line 673
    # this is here for non_GC languages like Odin, it is a no_op for GC languages like Python#line 674
    return  s                                               #line 675#line 676#line 677

def string_clone (s):                                       #line 678
    return  s                                               #line 679#line 680#line 681

# usage: app ${_00_} ${_0D_} arg main diagram_filename1 diagram_filename2 ...#line 682
# where ${_00_} is the root directory for the project       #line 683
# where ${_0D_} is the root directory for 0D (e.g. 0D/odin or 0D/python)#line 684#line 685
def initialize_component_palette (root_project,root_0D,diagram_source_files):#line 686
    reg = make_component_registry ()                        #line 687
    for diagram_source in  diagram_source_files:            #line 688
        all_containers_within_single_file = json2internal ( root_project, diagram_source)#line 689
        reg = generate_shell_components ( reg, all_containers_within_single_file)#line 690
        for container in  all_containers_within_single_file:#line 691
            register_component ( reg,mkTemplate ( container [ "name"], container, container_instantiator))#line 692#line 693#line 694
    initialize_stock_components ( reg)                      #line 695
    return  reg                                             #line 696#line 697#line 698

def print_error_maybe (main_container):                     #line 699
    error_port =  "✗"                                       #line 700
    err = fetch_first_output ( main_container, error_port)  #line 701
    if ( err!= None) and ( 0 < len (trimws ( err.v))):      #line 702
        print ( "___ !!! ERRORS !!! ___")                   #line 703
        print_specific_output ( main_container, error_port) #line 704#line 705#line 706#line 707

# debugging helpers                                         #line 708#line 709
def nl ():                                                  #line 710
    print ( "")                                             #line 711#line 712#line 713

def dump_outputs (main_container):                          #line 714
    nl ()                                                   #line 715
    print ( "___ Outputs ___")                              #line 716
    print ("[")
    print_output_list ( main_container)                     #line 717#line 718#line 719
    print ("]")

def trimws (s):                                             #line 720
    # remove whitespace from front and back of string       #line 721
    return  s.strip ()                                      #line 722#line 723#line 724

def clone_string (s):                                       #line 725
    return  s                                               #line 726#line 727#line 728

load_errors =  False                                        #line 729
runtime_errors =  False                                     #line 730#line 731
def load_error (s):                                         #line 732
    global load_errors                                      #line 733
    print ( s)                                              #line 734
    print ()                                                #line 735
    load_errors =  True                                     #line 736#line 737#line 738

def runtime_error (s):                                      #line 739
    global runtime_errors                                   #line 740
    print ( s)                                              #line 741
    runtime_errors =  True                                  #line 742#line 743#line 744
                                                            #line 745
def argv ():                                                #line 746
    return  sys.argv                                        #line 747#line 748#line 749

def initialize ():                                          #line 750
    root_of_project =  sys.argv[ 1]                         #line 751
    root_of_0D =  sys.argv[ 2]                              #line 752
    arg =  sys.argv[ 3]                                     #line 753
    main_container_name =  sys.argv[ 4]                     #line 754
    diagram_names =  sys.argv[ 5:]                          #line 755
    palette = initialize_component_palette ( root_of_project, root_of_0D, diagram_names)#line 756
    return [ palette,[ root_of_project, root_of_0D, main_container_name, diagram_names, arg]]#line 757#line 758#line 759

def start (palette,env):
    start_helper ( palette, env, False)                     #line 760

def start_show_all (palette,env):
    start_helper ( palette, env, True)                      #line 761

def start_helper (palette,env,show_all_outputs):            #line 762
    root_of_project =  env [ 0]                             #line 763
    root_of_0D =  env [ 1]                                  #line 764
    main_container_name =  env [ 2]                         #line 765
    diagram_names =  env [ 3]                               #line 766
    arg =  env [ 4]                                         #line 767
    set_environment ( root_of_project, root_of_0D)          #line 768
    # get entrypoint container                              #line 769
    main_container = get_component_instance ( palette, main_container_name, None)#line 770
    if  None ==  main_container:                            #line 771
        load_error ( str( "Couldn't find container with page name /") +  str( main_container_name) +  str( "/ in files ") +  str(str ( diagram_names)) +  " (check tab names, or disable compression?)"    )#line 775#line 776
    if not  load_errors:                                    #line 777
        marg = new_datum_string ( arg)                      #line 778
        msg = make_message ( "", marg)                      #line 779
        inject ( main_container, msg)                       #line 780
        if  show_all_outputs:                               #line 781
            dump_outputs ( main_container)                  #line 782
        else:                                               #line 783
            print_error_maybe ( main_container)             #line 784
            outp = fetch_first_output ( main_container, "") #line 785
            if  None ==  outp:                              #line 786
                print ("")
            else:                                           #line 788
                print_specific_output ( main_container, "") #line 789#line 790#line 791
        if  show_all_outputs:                               #line 792
            print ( "--- done ---")                         #line 793#line 794#line 795#line 796#line 797
                                                            #line 798
# utility functions                                         #line 799
def send_int (eh,port,i,causing_message):                   #line 800
    datum = new_datum_string (str ( i))                     #line 801
    send ( eh, port, datum, causing_message)                #line 802#line 803#line 804

def send_bang (eh,port,causing_message):                    #line 805
    datum = new_datum_bang ()                               #line 806
    send ( eh, port, datum, causing_message)                #line 807#line 808







def probeA_instantiate (reg,owner,name,template_data):      #line 1
    name_with_id = gensymbol ( "?A")                        #line 2
    return make_leaf ( name_with_id, owner, None, probe_handler)#line 3#line 4#line 5

def probeB_instantiate (reg,owner,name,template_data):      #line 6
    name_with_id = gensymbol ( "?B")                        #line 7
    return make_leaf ( name_with_id, owner, None, probe_handler)#line 8#line 9#line 10

def probeC_instantiate (reg,owner,name,template_data):      #line 11
    name_with_id = gensymbol ( "?C")                        #line 12
    return make_leaf ( name_with_id, owner, None, probe_handler)#line 13#line 14#line 15

def probe_handler (eh,msg):                                 #line 16
    global ticktime                                         #line 17
    s =  msg.datum.v                                        #line 18
    scontinued = ''
    if len (s) > 0:
        scontinued = '...'
    s = str( "  [") +  str(str ( ticktime)) +  str( "] ") +  str( "probe ") +  str( eh.name) +  str( ": ") +   s[:30].replace ('\r','').replace ('\n', '.') #line 25#line 26#line 27
    print (s[s.rindex('.')+1:] + scontinued, file=sys.stderr)

def trash_instantiate (reg,owner,name,template_data):       #line 28
    name_with_id = gensymbol ( "trash")                     #line 29
    return make_leaf ( name_with_id, owner, None, trash_handler)#line 30#line 31#line 32

def trash_handler (eh,msg):                                 #line 33
    # to appease dumped_on_floor checker                    #line 34
    pass                                                    #line 35#line 36

class TwoMessages:
    def __init__ (self,):                                   #line 37
        self.firstmsg =  None                               #line 38
        self.secondmsg =  None                              #line 39#line 40
                                                            #line 41
# Deracer_States :: enum { idle, waitingForFirstmsg, waitingForSecondmsg }#line 42
class Deracer_Instance_Data:
    def __init__ (self,):                                   #line 43
        self.state =  None                                  #line 44
        self.buffer =  None                                 #line 45#line 46
                                                            #line 47
def reclaim_Buffers_from_heap (inst):                       #line 48
    pass                                                    #line 49#line 50#line 51

def deracer_instantiate (reg,owner,name,template_data):     #line 52
    name_with_id = gensymbol ( "deracer")                   #line 53
    inst =  Deracer_Instance_Data ()                        #line 54
    inst.state =  "idle"                                    #line 55
    inst.buffer =  TwoMessages ()                           #line 56
    eh = make_leaf ( name_with_id, owner, inst, deracer_handler)#line 57
    return  eh                                              #line 58#line 59#line 60

def send_firstmsg_then_secondmsg (eh,inst):                 #line 61
    forward ( eh, "1", inst.buffer.firstmsg)                #line 62
    forward ( eh, "2", inst.buffer.secondmsg)               #line 63
    reclaim_Buffers_from_heap ( inst)                       #line 64#line 65#line 66

def deracer_handler (eh,msg):                               #line 67
    inst =  eh.instance_data                                #line 68
    if  inst.state ==  "idle":                              #line 69
        if  "1" ==  msg.port:                               #line 70
            inst.buffer.firstmsg =  msg                     #line 71
            inst.state =  "waitingForSecondmsg"             #line 72
        elif  "2" ==  msg.port:                             #line 73
            inst.buffer.secondmsg =  msg                    #line 74
            inst.state =  "waitingForFirstmsg"              #line 75
        else:                                               #line 76
            runtime_error ( str( "bad msg.port (case A) for deracer ") +  msg.port )#line 77#line 78
    elif  inst.state ==  "waitingForFirstmsg":              #line 79
        if  "1" ==  msg.port:                               #line 80
            inst.buffer.firstmsg =  msg                     #line 81
            send_firstmsg_then_secondmsg ( eh, inst)        #line 82
            inst.state =  "idle"                            #line 83
        else:                                               #line 84
            runtime_error ( str( "bad msg.port (case B) for deracer ") +  msg.port )#line 85#line 86
    elif  inst.state ==  "waitingForSecondmsg":             #line 87
        if  "2" ==  msg.port:                               #line 88
            inst.buffer.secondmsg =  msg                    #line 89
            send_firstmsg_then_secondmsg ( eh, inst)        #line 90
            inst.state =  "idle"                            #line 91
        else:                                               #line 92
            runtime_error ( str( "bad msg.port (case C) for deracer ") +  msg.port )#line 93#line 94
    else:                                                   #line 95
        runtime_error ( "bad state for deracer {eh.state}") #line 96#line 97#line 98#line 99

def low_level_read_text_file_instantiate (reg,owner,name,template_data):#line 100
    name_with_id = gensymbol ( "Low Level Read Text File")  #line 101
    return make_leaf ( name_with_id, owner, None, low_level_read_text_file_handler)#line 102#line 103#line 104

def low_level_read_text_file_handler (eh,msg):              #line 105
    fname =  msg.datum.v                                    #line 106

    try:
        f = open (fname)
    except Exception as e:
        f = None
    if f != None:
        data = f.read ()
        if data!= None:
            send_string (eh, "", data, msg)
        else:
            send_string (eh, "✗", f"read error on file '{fname}'", msg)
        f.close ()
    else:
        send_string (eh, "✗", f"open error on file '{fname}'", msg)
                                                            #line 107#line 108#line 109

def ensure_string_datum_instantiate (reg,owner,name,template_data):#line 110
    name_with_id = gensymbol ( "Ensure String Datum")       #line 111
    return make_leaf ( name_with_id, owner, None, ensure_string_datum_handler)#line 112#line 113#line 114

def ensure_string_datum_handler (eh,msg):                   #line 115
    if  "string" ==  msg.datum.kind ():                     #line 116
        forward ( eh, "", msg)                              #line 117
    else:                                                   #line 118
        emsg =  str( "*** ensure: type error (expected a string datum) but got ") +  msg.datum #line 119
        send_string ( eh, "✗", emsg, msg)                   #line 120#line 121#line 122#line 123

class Syncfilewrite_Data:
    def __init__ (self,):                                   #line 124
        self.filename =  ""                                 #line 125#line 126
                                                            #line 127
# temp copy for bootstrap, sends “done“ (error during bootstrap if not wired)#line 128
def syncfilewrite_instantiate (reg,owner,name,template_data):#line 129
    name_with_id = gensymbol ( "syncfilewrite")             #line 130
    inst =  Syncfilewrite_Data ()                           #line 131
    return make_leaf ( name_with_id, owner, inst, syncfilewrite_handler)#line 132#line 133#line 134

def syncfilewrite_handler (eh,msg):                         #line 135
    inst =  eh.instance_data                                #line 136
    if  "filename" ==  msg.port:                            #line 137
        inst.filename =  msg.datum.v                        #line 138
    elif  "input" ==  msg.port:                             #line 139
        contents =  msg.datum.v                             #line 140
        f = open ( inst.filename, "w")                      #line 141
        if  f!= None:                                       #line 142
            f.write ( msg.datum.v)                          #line 143
            f.close ()                                      #line 144
            send ( eh, "done",new_datum_bang (), msg)       #line 145
        else:                                               #line 146
            send_string ( eh, "✗", str( "open error on file ") +  inst.filename , msg)#line 147#line 148#line 149#line 150#line 151

class StringConcat_Instance_Data:
    def __init__ (self,):                                   #line 152
        self.buffer1 =  None                                #line 153
        self.buffer2 =  None                                #line 154#line 155
                                                            #line 156
def stringconcat_instantiate (reg,owner,name,template_data):#line 157
    name_with_id = gensymbol ( "stringconcat")              #line 158
    instp =  StringConcat_Instance_Data ()                  #line 159
    return make_leaf ( name_with_id, owner, instp, stringconcat_handler)#line 160#line 161#line 162

def stringconcat_handler (eh,msg):                          #line 163
    inst =  eh.instance_data                                #line 164
    if  "1" ==  msg.port:                                   #line 165
        inst.buffer1 = clone_string ( msg.datum.v)          #line 166
        maybe_stringconcat ( eh, inst, msg)                 #line 167
    elif  "2" ==  msg.port:                                 #line 168
        inst.buffer2 = clone_string ( msg.datum.v)          #line 169
        maybe_stringconcat ( eh, inst, msg)                 #line 170
    elif  "reset" ==  msg.port:                             #line 171
        inst.buffer1 =  None                                #line 172
        inst.buffer2 =  None                                #line 173
    else:                                                   #line 174
        runtime_error ( str( "bad msg.port for stringconcat: ") +  msg.port )#line 175#line 176#line 177#line 178

def maybe_stringconcat (eh,inst,msg):                       #line 179
    if  inst.buffer1!= None and  inst.buffer2!= None:       #line 180
        concatenated_string =  ""                           #line 181
        if  0 == len ( inst.buffer1):                       #line 182
            concatenated_string =  inst.buffer2             #line 183
        elif  0 == len ( inst.buffer2):                     #line 184
            concatenated_string =  inst.buffer1             #line 185
        else:                                               #line 186
            concatenated_string =  inst.buffer1+ inst.buffer2#line 187#line 188
        send_string ( eh, "", concatenated_string, msg)     #line 189
        inst.buffer1 =  None                                #line 190
        inst.buffer2 =  None                                #line 191#line 192#line 193#line 194

#                                                           #line 195#line 196
def string_constant_instantiate (reg,owner,name,template_data):#line 197
    global root_project                                     #line 198
    global root_0D                                          #line 199
    name_with_id = gensymbol ( "strconst")                  #line 200
    s =  template_data                                      #line 201
    if  root_project!= "":                                  #line 202
        s = re.sub ( "_00_",  root_project,  s)             #line 203#line 204
    if  root_0D!= "":                                       #line 205
        s = re.sub ( "_0D_",  root_0D,  s)                  #line 206#line 207
    return make_leaf ( name_with_id, owner, s, string_constant_handler)#line 208#line 209#line 210

def string_constant_handler (eh,msg):                       #line 211
    s =  eh.instance_data                                   #line 212
    send_string ( eh, "", s, msg)                           #line 213#line 214#line 215

def fakepipename_instantiate (reg,owner,name,template_data):#line 216
    instance_name = gensymbol ( "fakepipe")                 #line 217
    return make_leaf ( instance_name, owner, None, fakepipename_handler)#line 218#line 219#line 220

rand =  0                                                   #line 221#line 222
def fakepipename_handler (eh,msg):                          #line 223
    global rand                                             #line 224
    rand =  rand+ 1
    # not very random, but good enough _ ;rand' must be unique within a single run#line 225
    send_string ( eh, "", str( "/tmp/fakepipe") +  rand , msg)#line 226#line 227#line 228
                                                            #line 229
class Switch1star_Instance_Data:
    def __init__ (self,):                                   #line 230
        self.state =  "1"                                   #line 231#line 232
                                                            #line 233
def switch1star_instantiate (reg,owner,name,template_data): #line 234
    name_with_id = gensymbol ( "switch1*")                  #line 235
    instp =  Switch1star_Instance_Data ()                   #line 236
    return make_leaf ( name_with_id, owner, instp, switch1star_handler)#line 237#line 238#line 239

def switch1star_handler (eh,msg):                           #line 240
    inst =  eh.instance_data                                #line 241
    whichOutput =  inst.state                               #line 242
    if  "" ==  msg.port:                                    #line 243
        if  "1" ==  whichOutput:                            #line 244
            forward ( eh, "1", msg)                         #line 245
            inst.state =  "*"                               #line 246
        elif  "*" ==  whichOutput:                          #line 247
            forward ( eh, "*", msg)                         #line 248
        else:                                               #line 249
            send ( eh, "✗", "internal error bad state in switch1*", msg)#line 250#line 251
    elif  "reset" ==  msg.port:                             #line 252
        inst.state =  "1"                                   #line 253
    else:                                                   #line 254
        send ( eh, "✗", "internal error bad message for switch1*", msg)#line 255#line 256#line 257#line 258

class Latch_Instance_Data:
    def __init__ (self,):                                   #line 259
        self.datum =  None                                  #line 260#line 261
                                                            #line 262
def latch_instantiate (reg,owner,name,template_data):       #line 263
    name_with_id = gensymbol ( "latch")                     #line 264
    instp =  Latch_Instance_Data ()                         #line 265
    return make_leaf ( name_with_id, owner, instp, latch_handler)#line 266#line 267#line 268

def latch_handler (eh,msg):                                 #line 269
    inst =  eh.instance_data                                #line 270
    if  "" ==  msg.port:                                    #line 271
        inst.datum =  msg.datum                             #line 272
    elif  "release" ==  msg.port:                           #line 273
        d =  inst.datum                                     #line 274
        if  d ==  None:                                     #line 275
            send_string ( eh, "", "", msg)                  #line 276
            print ( " warning: *** latch sending empty string ***", file=sys.stderr)#line 277
        else:                                               #line 278
            send ( eh, "", d, msg)                          #line 279#line 280
        inst.datum =  None                                  #line 281
    else:                                                   #line 282
        send ( eh, "✗", "internal error bad message for latch", msg)#line 283#line 284#line 285#line 286

# all of the the built_in leaves are listed here            #line 287
# future: refactor this such that programmers can pick and choose which (lumps of) builtins are used in a specific project#line 288#line 289
def initialize_stock_components (reg):                      #line 290
    register_component ( reg,mkTemplate ( "1then2", None, deracer_instantiate))#line 291
    register_component ( reg,mkTemplate ( "?A", None, probeA_instantiate))#line 292
    register_component ( reg,mkTemplate ( "?B", None, probeB_instantiate))#line 293
    register_component ( reg,mkTemplate ( "?C", None, probeC_instantiate))#line 294
    register_component ( reg,mkTemplate ( "trash", None, trash_instantiate))#line 295#line 296
    register_component ( reg,mkTemplate ( "Read Text File", None, low_level_read_text_file_instantiate))#line 297
    register_component ( reg,mkTemplate ( "Ensure String Datum", None, ensure_string_datum_instantiate))#line 298#line 299
    register_component ( reg,mkTemplate ( "syncfilewrite", None, syncfilewrite_instantiate))#line 300
    register_component ( reg,mkTemplate ( "stringconcat", None, stringconcat_instantiate))#line 301
    register_component ( reg,mkTemplate ( "switch1*", None, switch1star_instantiate))#line 302
    register_component ( reg,mkTemplate ( "latch", None, latch_instantiate))#line 303
    # for fakepipe                                          #line 304
    register_component ( reg,mkTemplate ( "fakepipename", None, fakepipename_instantiate))#line 305#line 306#line 307







# this needs to be rewritten to use the low_level “shell_out“ component, this can be done solely as a diagram without using python code here#line 1
def shell_out_instantiate (reg,owner,name,template_data):   #line 2
    name_with_id = gensymbol ( "shell_out")                 #line 3
    cmd = shlex.split ( template_data)                      #line 4
    return make_leaf ( name_with_id, owner, cmd, shell_out_handler)#line 5#line 6#line 7

def shell_out_handler (eh,msg):                             #line 8
    cmd =  eh.instance_data                                 #line 9
    s =  msg.datum.v                                        #line 10
    ret =  None                                             #line 11
    rc =  None                                              #line 12
    stdout =  None                                          #line 13
    stderr =  None                                          #line 14

    try:
        ret = subprocess.run ( cmd, input= s, text=True, capture_output=True)
        rc = ret.returncode
        stdout = ret.stdout.strip ()
        stderr = ret.stderr.strip ()
    except Exception as e:
        ret = None
        rc = 1
        stdout = ''
        stderr = str(e)
                                                            #line 15
    if  rc!= 0:                                             #line 16
        send_string ( eh, "✗", stderr, msg)                 #line 17
    else:                                                   #line 18
        send_string ( eh, "", stdout, msg)                  #line 19#line 20#line 21#line 22

def generate_shell_components (reg,container_list):         #line 23
    # [                                                     #line 24
    #     {;file': 'simple0d.drawio', 'name': 'main', 'children': [{'name': 'Echo', 'id': 5}], 'connections': [...]},#line 25
    #     {'file': 'simple0d.drawio', 'name': '...', 'children': [], 'connections': []}#line 26
    # ]                                                     #line 27
    if  None!= container_list:                              #line 28
        for diagram in  container_list:                     #line 29
            # loop through every component in the diagram and look for names that start with “$“ or “'“ #line 30
            # {'file': 'simple0d.drawio', 'name': 'main', 'children': [{'name': 'Echo', 'id': 5}], 'connections': [...]},#line 31
            for child_descriptor in  diagram [ "children"]: #line 32
                if first_char_is ( child_descriptor [ "name"], "$"):#line 33
                    name =  child_descriptor [ "name"]      #line 34
                    cmd =   name[1:] .strip ()              #line 35
                    generated_leaf = mkTemplate ( name, cmd, shell_out_instantiate)#line 36
                    register_component ( reg, generated_leaf)#line 37
                elif first_char_is ( child_descriptor [ "name"], "'"):#line 38
                    name =  child_descriptor [ "name"]      #line 39
                    s =   name[1:]                          #line 40
                    generated_leaf = mkTemplate ( name, s, string_constant_instantiate)#line 41
                    register_component_allow_overwriting ( reg, generated_leaf)#line 42#line 43#line 44#line 45#line 46
    return  reg                                             #line 47#line 48#line 49

def first_char (s):                                         #line 50
    return   s[0]                                           #line 51#line 52#line 53

def first_char_is (s,c):                                    #line 54
    return  c == first_char ( s)                            #line 55#line 56#line 57
                                                            #line 58
# TODO: #run_command needs to be rewritten to use the low_level “shell_out“ component, this can be done solely as a diagram without using python code here#line 59
# I'll keep it for now, during bootstrapping, since it mimics what is done in the Odin prototype _ both need to be revamped#line 60#line 61






count_counter =  0                                          #line 1
count_direction =  1                                        #line 2#line 3
def count_handler (eh,msg):                                 #line 4
    global count_counter, count_direction                   #line 5
    if  msg.port ==  "adv":                                 #line 6
        count_counter =  count_counter+ count_direction     #line 7
        send_int ( eh, "", count_counter, msg)              #line 8
    elif  msg.port ==  "rev":                               #line 9
        count_direction = - count_direction                 #line 10#line 11#line 12#line 13

def count_instantiator (reg,owner,name,template_data):      #line 14
    name_with_id = gensymbol ( "Count")                     #line 15
    return make_leaf ( name_with_id, owner, None, count_handler)#line 16#line 17#line 18

def count_install (reg):                                    #line 19
    register_component ( reg,mkTemplate ( "Count", None, count_instantiator))#line 20#line 21







def decode_install (reg):                                   #line 1
    register_component ( reg,mkTemplate ( "Decode", None, decode_instantiator))#line 2#line 3#line 4

def decode_handler (eh,msg):                                #line 5
    global decode_digits                                    #line 6
    s =  msg.datum.v                                        #line 7
    i = int ( s)                                            #line 8
    if  i >=  0 and  i <=  9:                               #line 9
        send_string ( eh, s, s, msg)                        #line 10#line 11
    send_bang ( eh, "done", msg)                            #line 12#line 13#line 14

def decode_instantiator (reg,owner,name,template_data):     #line 15
    name_with_id = gensymbol ( "Decode")                    #line 16
    return make_leaf ( name_with_id, owner, None, decode_handler)#line 17







def reverser_install (reg):                                 #line 1
    register_component ( reg,mkTemplate ( "Reverser", None, reverser_instantiator))#line 2#line 3#line 4

reverser_state =  "J"                                       #line 5#line 6
def reverser_handler (eh,msg):                              #line 7
    global reverser_state                                   #line 8
    if  reverser_state ==  "K":                             #line 9
        if  msg.port ==  "J":                               #line 10
            send_bang ( eh, "", msg)                        #line 11
            reverser_state =  "J"                           #line 12
        else:                                               #line 13
            pass                                            #line 14#line 15
    elif  reverser_state ==  "J":                           #line 16
        if  msg.port ==  "K":                               #line 17
            send_bang ( eh, "", msg)                        #line 18
            reverser_state =  "K"                           #line 19
        else:                                               #line 20
            pass                                            #line 21#line 22#line 23#line 24#line 25

def reverser_instantiator (reg,owner,name,template_data):   #line 26
    name_with_id = gensymbol ( "Reverser")                  #line 27
    return make_leaf ( name_with_id, owner, None, reverser_handler)#line 28#line 29







def delay_install (reg):                                    #line 1
    register_component ( reg,mkTemplate ( "Delay", None, delay_instantiator))#line 2#line 3#line 4

class Delay_Info:
    def __init__ (self,):                                   #line 5
        self.counter =  0                                   #line 6
        self.saved_message =  None                          #line 7#line 8
                                                            #line 9
def delay_instantiator (reg,owner,name,template_data):      #line 10
    name_with_id = gensymbol ( "delay")                     #line 11
    info =  Delay_Info ()                                   #line 12
    return make_leaf ( name_with_id, owner, info, delay_handler)#line 13#line 14#line 15

DELAYDELAY =  5000                                          #line 16#line 17
def first_time (m):                                         #line 18
    return not is_tick ( m)                                 #line 19#line 20#line 21

def delay_handler (eh,msg):                                 #line 22
    info =  eh.instance_data                                #line 23
    if first_time ( msg):                                   #line 24
        info.saved_message =  msg                           #line 25
        set_active ( eh)
        # tell engine to keep running this component with ;ticks' #line 26#line 27#line 28
    count =  info.counter                                   #line 29
    next =  count+ 1                                        #line 30
    if  info.counter >=  DELAYDELAY:                        #line 31
        set_idle ( eh)
        # tell engine that we're finally done               #line 32
        forward ( eh, "", info.saved_message)               #line 33
        next =  0                                           #line 34#line 35
    info.counter =  next                                    #line 36#line 37#line 38







def monitor_install (reg):                                  #line 1
    register_component ( reg,mkTemplate ( "@", None, monitor_instantiator))#line 2#line 3#line 4

def monitor_instantiator (reg,owner,name,template_data):    #line 5
    name_with_id = gensymbol ( "@")                         #line 6
    return make_leaf ( name_with_id, owner, None, monitor_handler)#line 7#line 8#line 9

def monitor_handler (eh,msg):                               #line 10
    s =  msg.datum.v                                        #line 11
    i = int ( s)                                            #line 12
    while  i >  0:                                          #line 13
        s =  str( " ") +  s                                 #line 14
        i =  i- 1                                           #line 15#line 16
    print ( s)                                              #line 17#line 18





