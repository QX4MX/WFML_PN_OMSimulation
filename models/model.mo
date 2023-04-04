
    model PNLibComponentsOverview
        PNlib.Components.PD p1(nIn = 0,nOut = 1, startTokens = 1);
        PNlib.Components.PD p2(nIn = 1, nOut = 0, startTokens = 0);
        PNlib.Components.T t1(arcWeightIn = {1}, arcWeightOut = {1},nIn = 1, nOut = 1);
    equation
        connect(p1.outTransition[1], t1.inPlaces[1]);
        connect(t1.outPlaces[1], p2.inTransition[1]);
          annotation(
            uses(PNlib(version = "2.2")));
    end PNLibComponentsOverview;

