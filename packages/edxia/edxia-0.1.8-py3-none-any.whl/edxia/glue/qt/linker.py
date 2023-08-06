# Copyright (c) 2019 Fabien Georget <fabien.georget@epfl.ch>, EPFL
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from glue.config import menubar_plugin
from glue.core.component_link import ComponentLink
from glue.core.component_id import ComponentID
from glue.core.parse import ParsedCommand, ParsedComponentLink

import qtpy.QtWidgets as qtw
import qtpy.QtGui as qtg
import qtpy.QtCore as qtc

from edxia.utils.chemistry import molar_masses
from edxia.utils.qt import set_busy_app

from edxia.glue.phase_data import PhaseData

components = list(molar_masses.keys())
components.append("BSE")
components.append("SOX")

def pts_ratios(numer, denom):
    return numer/denom

@menubar_plugin("edxia: Link EDS components")
@set_busy_app
def component_linker(session, data_collection):

    datas = data_collection.data
    links = []
    for ind, data in enumerate(datas):
        for component in components:
            cid = data.find_component_id(component)
            if cid is not None:
                # Link to other components
                for ind2, data2 in enumerate(datas):
                    if ind2 <= ind:
                        continue
                    cid2 = data2.find_component_id(component)
                    if cid2 is not None:
                        links.append(ComponentLink([cid,], cid2))
                # Ratio links
                if isinstance(data, PhaseData):
                    continue
                if component in ["Al", "S", "Cl", "Mg", "Si", "Fe"]:
                    cid_ca = data.find_component_id("Ca")
                    if cid_ca is not None:
                        # Define the ratios as ParsedCommand so they appear in the editor
                        equation = "{"+component+"}/{Ca}"
                        references = {"Ca": cid_ca, component: cid}
                        cmd = ParsedCommand(equation, references)
                        label = component+"/Ca"
                        # only add if not already created
                        if  data.find_component_id(label) is None:
                            ratio = ComponentID(label)
                            link = ParsedComponentLink(ratio, cmd)
                            link.compute(data)
                            data.add_component_link(link) # this is sufficient
                                                          # to add it to the
                                                          # interface

    data_collection.set_links(links)



