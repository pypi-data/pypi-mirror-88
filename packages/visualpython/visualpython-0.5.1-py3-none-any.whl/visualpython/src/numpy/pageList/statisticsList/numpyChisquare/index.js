define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpFuncJS'

    // numpy 패키지를 위한 라이브러리import 
    , 'nbextensions/visualpython/src/numpy/constant_numpy'
    , 'nbextensions/visualpython/src/numpy/api/numpyStateApi'
    , 'nbextensions/visualpython/src/numpy/api/numpyRouteMapApi'
    , 'nbextensions/visualpython/src/numpy/api/numpyValidatorApi'

], function ( requirejs, $, vpCommon, vpConst, sb, vpFuncJS, 
              vpNumpyConst, numpyStateApi, numpyRouteMapApi, numpyValidatorApi ) {
    // 옵션 속성
    const funcOptProp = {
        stepCount : 1
        , funcName : "numpyChisquare"
        , funcID : "JY209"  // TODO: ID 규칙 생성 필요
    }

    // FuncId에 맞는 FuncData를 맵핑하는 api
    const { newMapFuncIdToNumpyFuncData, mapFuncIdToHtmlUrlPath } = numpyRouteMapApi;
    const { validateNumpyState } = numpyValidatorApi;

    /**
     * html load 콜백. 고유 id 생성하여 부과하며 js 객체 클래스 생성하여 컨테이너로 전달
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     */
    var optionLoadCallback = function(callback) {
        // document.getElementsByTagName("head")[0].appendChild(link);
        // 컨테이너에서 전달된 callback 함수가 존재하면 실행.
        if (typeof(callback) === 'function') {
            var uuid = vpCommon.getUUID();
            // 최대 10회 중복되지 않도록 체크
            for (var idx = 0; idx < 10; idx++) {
                // 이미 사용중인 uuid 인 경우 다시 생성
                if ($(vpConst.VP_CONTAINER_ID).find("." + uuid).length > 0) {
                    uuid = vpCommon.getUUID();
                }
            }
            $(vpCommon.wrapSelector(vpConst.OPTION_GREEN_ROOM)).find(vpConst.OPTION_PAGE).addClass(uuid);
            // 옵션 객체 생성
            var ipImport = new ImportPackage(uuid);
            // 옵션 속성 할당.
            ipImport.setOptionProp(funcOptProp);
            // html 설정.
            ipImport.initHtml();
            callback(ipImport);  // 공통 객체를 callback 인자로 전달
        }
    }

    /**
     * html 로드. 
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
    */
    var initOption = function(callback) {
        var htmlUrlPath  = mapFuncIdToHtmlUrlPath(funcOptProp.funcID);
        vpCommon.loadHtml(vpCommon.wrapSelector(vpConst.OPTION_GREEN_ROOM), htmlUrlPath, optionLoadCallback, callback);
    }

   
    /**
     * 본 옵션 처리 위한 클래스
     * @param {String} uuid 고유 id
     */
    var ImportPackage = function(uuid) {
        this.uuid = uuid; // Load html 영역의 uuid.
        this.numpyCodeGenerator  // numpyCodeGenerator은 코드를 만듬
        // this.numpyCodeValidator // numpyCodeValidator은 코드 실행 전 입력된 state 값을 검증
        this.numpyPageRender // numpyPageRender는 동적 html을 index.html에 렌더링
        this.numpyStateGenerator // numpyStateGenerator는 state를 생성, 변경 
    }

    /**
     * vpFuncJS 에서 상속
    */
    ImportPackage.prototype = Object.create(vpFuncJS.VpFuncJS.prototype);

    /**
     * 유효성 검사
     * @returns 유효성 검사 결과. 적합시 true
     */
    ImportPackage.prototype.optionValidation = function() {
        // state 데이터를 validation 한다
        return validateNumpyState();
    }

    /**
     * html 내부 binding 처리
     */
    ImportPackage.prototype.initHtml = function() {
        var { numpyCodeGenerator
            // , numpyCodeValidator
            , numpyPageRender
            , numpyStateGenerator } = newMapFuncIdToNumpyFuncData(funcOptProp.funcID);
        this.numpyCodeGenerator = numpyCodeGenerator;
        // this.numpyCodeValidator = numpyCodeValidator;
        this.numpyPageRender = numpyPageRender;
        this.numpyStateGenerator = numpyStateGenerator;

        //importPackageThis와 동적 html 태그들을 index.html에 렌더링 
        this.numpyPageRender.setImportPackageThis(this);
        this.numpyPageRender.pageRender();

        // import load css
        this.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + vpNumpyConst.NUMPY_BASE_CSS_PATH);
    }

    /**
     *  페이지에 생성된 uuid를 가져온다
     */
    ImportPackage.prototype.getUUID = function() {
        return this.uuid;
    }
    
    /**
     * 코드 생성
     * @param {boolean} exec 실행여부
     */
    ImportPackage.prototype.generateCode = function(exec) {
        // validate code 
        if (!this.optionValidation()) return;
        // make code
        this.numpyCodeGenerator.makeCode();
        var result = this.numpyCodeGenerator.getCodeAndClear();
        if (result == null) return "BREAK_RUN"; // 코드 생성 중 오류 발생
        // execute code
        this.cellExecute(result, exec);
    }

    return {
        initOption: initOption
    };
});
