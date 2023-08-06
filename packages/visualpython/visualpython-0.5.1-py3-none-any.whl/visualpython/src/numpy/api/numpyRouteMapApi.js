define ([
    'require'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/vpCommon'
    //
    , '../constant_numpy'
], function(requirejs, vpConst, vpCommon
            , vpNumpyConst ) {
    "use strict";

    var NUMPY_PROP_MAP = vpNumpyConst.NUMPY_PROP_MAP;

    /** FuncId에 맞는 HtmlUrlPath를 맵핑하는 api */
    var mapFuncIdToHtmlUrlPath = function( funcId ) {
        return 'numpy/pageList/index.html';
    }

    /** @old 
     *  FuncId에 맞는 FuncData를 맵핑하고 
     * FuncId마다 다른 numpyCodeGenerator, numpyCodeValidator numpyPageRender numpyStateGenerator의
     * 인스턴스를 생성하는 api 함수
     *  api */
    var newMapFuncIdToNumpyFuncData = function( funcId, funcName ) {
        if (NUMPY_PROP_MAP.has(funcId) === false) {
            // FIXME: NUMPY_PROP_MAP 객체에 funcId가 없을 때 에러 처리
            alert("NUMPY_PROP_MAP not has funcId");
            return;
        }

        var numpyOptionObj = NUMPY_PROP_MAP.get(funcId).numpyOptionObj;

        var numpyCodeGenerator = new ( NUMPY_PROP_MAP.get(funcId).numpyCodeGenerator );
        // var numpyCodeValidator = new ( NUMPY_PROP_MAP.get(funcId).numpyCodeValidator );
        var numpyPageRender = new ( NUMPY_PROP_MAP.get(funcId).numpyPageRender )(numpyOptionObj);
        var numpyStateGenerator = new ( NUMPY_PROP_MAP.get(funcId).numpyStateGenerator );

        var htmlUrlPath = NUMPY_PROP_MAP.get(funcId).htmlUrlPath;
        var bluePrintReadOnlyState = { ...NUMPY_PROP_MAP.get(funcId).state };

        numpyStateGenerator.makeState(bluePrintReadOnlyState);
        var state = numpyStateGenerator.getStateAll();

        numpyCodeGenerator.setStateGenerator(numpyStateGenerator);
        numpyPageRender.setStateGenerator(numpyStateGenerator);
        
        return {
            numpyCodeGenerator
            // , numpyCodeValidator
            , numpyPageRender
            , numpyStateGenerator
            , htmlUrlPath
            , state
        }
    }

    return {
        mapFuncIdToHtmlUrlPath
        , newMapFuncIdToNumpyFuncData
    }
    
});