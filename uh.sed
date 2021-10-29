#!/bin/bash
sed
	-e 's/&lt;/</g' \
	-e 's/&gt;/>/g' \
	-e 's/&quot;/\'/' \
	-e 's/&amp;/\*/' \
