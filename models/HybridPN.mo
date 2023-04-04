model HybridPN
    PNlib.Components.PD PD_0(startTokens=3,nIn=0,nOut=1);
    PNlib.Components.PD PD_1(startTokens=1,nIn=1,nOut=0);
    PNlib.Components.PC PC_0(startMarks=3.5,nIn=0,nOut=1);
    PNlib.Components.PC PC_1(startMarks=1,nIn=1,nOut=0);
    PNlib.Components.TD TD(nIn=1,nOut=1,delay=1);
    PNlib.Components.TC TC(nIn=1,nOut=1,maximumSpeed=0.5);
    equation
        connect(PD_0.outTransition[1],TD.inPlaces[1]);
        connect(TD.outPlaces[1],PD_1.inTransition[1]);
        connect(PC_0.outTransition[1],TC.inPlaces[1]);
        connect(TC.outPlaces[1],PC_1.inTransition[1]);
    annotation(
        uses(PNlib(version = "2.2"))
    );
end HybridPN;