define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpFuncJS'
    , 'nbextensions/visualpython/src/container/vpContainer'
    , 'nbextensions/visualpython/src/pandas/common/pandasGenerator'
], function (requirejs, $, vpCommon, vpConst, sb, vpFuncJS, vpContainer, pdGen) {
    // 옵션 속성
    const funcOptProp = {
        stepCount : 1
        , funcName : "Import Matplotlib"
        , funcID : "mp_importMatplotlib"  // TODO: ID 규칙 생성 필요
    }

    /**
     * html load 콜백. 고유 id 생성하여 부과하며 js 객체 클래스 생성하여 컨테이너로 전달
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     */
    var optionLoadCallback = function(callback, meta) {
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
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_GREEN_ROOM))).find(vpCommon.formatString(".{0}", vpConst.API_OPTION_PAGE)).addClass(uuid);

            // 옵션 객체 생성
            var mpPackage = new MatplotPackage(uuid);
            mpPackage.metadata = meta;

            // 옵션 속성 할당.
            mpPackage.setOptionProp(funcOptProp);
            // html 설정.
            mpPackage.initHtml();
            callback(mpPackage);  // 공통 객체를 callback 인자로 전달
        }
    }
    
    /**
     * html 로드. 
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     */
    var initOption = function(callback, meta) {
        vpCommon.loadHtml(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_GREEN_ROOM)), "pandas/common/commonPandas.html", optionLoadCallback, callback, meta);
    }

    /**
     * 본 옵션 처리 위한 클래스
     * @param {String} uuid 고유 id
     */
    var MatplotPackage = function(uuid) {
        this.uuid = uuid;           // Load html 영역의 uuid.
        this.package = {
            code: 'import matplotlib.pyplot as ${i0}',
            input: [
                {
                    name: 'i0',
                    label: 'matplotlib.pyplot as',
                    type: 'int',
                    value: 'plt'
                }
            ],
            output: [],
            variable: [],
            postfix: [
                "%matplotlib inline"
                , ""
                , "#plt.style.use('fivethirtyeight')"
                , "#from matplotlib.pylab import rcParams"
                , "#rcParams['figure.figsize'] = 12, 8"
                , "#rcParams['axes.grid'] = True"
            ]
        }
    }

    /**
     * vpFuncJS 에서 상속
     */
    MatplotPackage.prototype = Object.create(vpFuncJS.VpFuncJS.prototype);

    /**
     * 유효성 검사
     * @returns 유효성 검사 결과. 적합시 true
     */
    MatplotPackage.prototype.optionValidation = function() {
        return true;

        // 부모 클래스 유효성 검사 호출.
        // vpFuncJS.VpFuncJS.prototype.optionValidation.apply(this);
    }


    /**
     * html 내부 binding 처리
     */
    MatplotPackage.prototype.initHtml = function() {
        this.showFunctionTitle();

        this.bindOptions();

        this.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + "pandas/commonPandas.css");
    }

    /**
     * 선택한 패키지명 입력
     */
    MatplotPackage.prototype.showFunctionTitle = function() {
        $(this.wrapSelector('.vp-funcNavi')).html(
            `
            <span class="vp-multilang" data-caption-id="funcNavi"> Matplotlib &gt; <strong><span data-caption-id="vp_functionName" class="vp_functionName">Import Matplotlib</span></strong></span>
            `
        )
        // $(this.wrapSelector('.vp_functionName')).text('Import Matplotlib');
    }

    /**
     * 패키지 바인딩
     */
    MatplotPackage.prototype.bindOptions = function() {
        // HTML 구성
        pdGen.vp_showInterface(this.wrapSelector(''), this.package);
        // if it has no additional options, remove that box
        if (this.package.variable == undefined || this.package.variable.length <= 0) {
            $(this.wrapSelector('#vp_optionBox')).closest('div.vp-accordion-container').remove();
        }

        // FIXME: 일단 이름 변경 막기
        $(this.wrapSelector('#i0')).attr('disabled', true);

        // matplotlib 설정값 주석으로 입력 FIXME: 추후엔 postfix/prefix code도 공통generator에서 작업
        var postCode = new sb.StringBuilder();
        this.package.postfix.forEach(code => {
            postCode.appendLine(code);
        })
        $(this.wrapSelector('#vp_postfixBox textarea')).val(postCode.toString());
    };

    /**
     * 코드 생성
     * @param {boolean} exec 실행여부
     */
    MatplotPackage.prototype.generateCode = function(addCell, exec) {
        if (!this.optionValidation()) return;

        try {
            var sbCode = new sb.StringBuilder();
            
            // add prefix code
            var prefixCode = $(this.wrapSelector('#vp_prefixBox textarea')).val();
            if (prefixCode.length > 0) {
                sbCode.appendLine(prefixCode);
            }

            // 코드 생성
            var result = pdGen.vp_codeGenerator(this.uuid, this.package);
            if (result == null) return "BREAK_RUN"; // 코드 생성 중 오류 발생
            sbCode.append(result);
            
            // cell metadata 작성하기
            // pdGen.vp_setCellMetadata(_VP_CODEMD);

            // add postfix code
            var postfix = $(this.wrapSelector('#vp_postfixBox textarea')).val();
            if (postfix.length > 0) {
                sbCode.appendLine('');
                sbCode.append(postfix);
            }

            // 코드 추가 및 실행
            if (addCell) this.cellExecute(sbCode.toString(), exec);
        } catch (exmsg) {
            // 에러 표시
            vpCommon.renderAlertModal(exmsg);
            return "BREAK_RUN"; // 코드 생성 중 오류 발생
        }

        return sbCode.toString();
    }

    return {
        initOption: initOption
    };
});