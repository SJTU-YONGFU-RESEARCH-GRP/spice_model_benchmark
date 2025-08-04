#! /bin/bash

export OPUSHOME=path_to_spiceopus
export PATH=.:${OPUSHOME}/bin:${PATH}
export LD_LIBRARY_PATH=.:${LD_LIBRARY_PATH}

spiceopus -pw . -o spiceopus.log spinit_local &

