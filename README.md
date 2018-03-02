# lofar-grid-stage
New staging scripts to use the updated GFAL2.

Usage
-----
**File status**

To check a single SURL by hand:

    python state_gfal2.py <surl>
To check a SURL from another script:

    import state_gfal2
    state_gfal2.check_status(surl)

**File staging**

As based on the example given here (alson included in this repository): https://gitlab.cern.ch/dmc/gfal2-bindings/blob/develop/example/python/gfal2_bring_online.py

To stage a single SURL by hand:

    python stage_gfal2.py <surl>
    
To stage from another script:

    import stage_gfal2
    stage_gfal2.stage(surl)

The original script on which this is based can stage with (does not exit until staging finshes or errors):

    python gfal2_bring_online.py <surl>
