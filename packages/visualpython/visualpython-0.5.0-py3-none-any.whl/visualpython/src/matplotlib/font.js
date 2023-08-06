define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpFuncJS'
    , 'nbextensions/visualpython/src/pandas/common/pandasGenerator'
], function (requirejs, $, vpCommon, vpConst, sb, vpFuncJS, pdGen) {
    // 옵션 속성
    const funcOptProp = {
        stepCount : 1
        , funcName : "Font Setting"
        , funcID : "mp_font"  // TODO: ID 규칙 생성 필요
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
        vpCommon.loadHtml(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_GREEN_ROOM)), "matplotlib/font.html", optionLoadCallback, callback, meta);
    }

    /**
     * 본 옵션 처리 위한 클래스
     * @param {String} uuid 고유 id
     */
    var MatplotPackage = function(uuid) {
        this.uuid = uuid;   // Load html 영역의 uuid.
        this.package = {
            input: [
                { name: 'vp_slctFontList' },
                { name: 'vp_txtFontSize' }
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
        this.bindFontSetting();

        this.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + "pandas/commonPandas.css");
        this.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + "matplotlib/plot.css");
    }

    /**
     * 선택한 패키지명 입력
     */
    MatplotPackage.prototype.showFunctionTitle = function() {
        $(this.wrapSelector('.vp_functionName')).text(this.funcName);
    }

    /**
     * Pandas 기본 패키지 바인딩
     */
    MatplotPackage.prototype.bindOptions = function() {
        
    };

    /**
     * 폰트 설정 바인딩
     */
    MatplotPackage.prototype.bindFontSetting = function() {
        var sbCmd = new sb.StringBuilder();
        sbCmd.appendLine("import matplotlib.font_manager as fm");
        sbCmd.appendLine("_ttflist = fm.fontManager.ttflist");
        sbCmd.append("print([{'name': f.name, 'path': f.fname, 'style':f.style, 'variant': f.variant} for f in _ttflist])");
        
        var that = this;
        this.kernelExecute(sbCmd.toString(), function (result) {
            var varList = JSON.parse(result.replace(/'/gi, `"`));
            
            // 데이터 프레임 select 태그 구성
            var sbTags = new sb.StringBuilder();
            varList.forEach(listVar => {
                // 한글 폰트로 default 설정
                if (listVar.name == 'Gulim' || listVar.name == 'New Gulim') {
                    sbTags.appendFormatLine("<option value='{0}' selected>{1}</option>", listVar.name, listVar.name);
                } else {
                    sbTags.appendFormatLine("<option value='{0}'>{1}</option>", listVar.name, listVar.name);
                }
            });

            $(that.wrapSelector("#vp_slctFontList")).html(sbTags.toString());
        });
    }

    /**
     * 코드 생성
     * @param {boolean} exec 실행여부
     */
    MatplotPackage.prototype.generateCode = function(addCell, exec) {
        if (!this.optionValidation()) return;
        
        var sbCode = new sb.StringBuilder();
        
        // add prefix code
        var prefixCode = $(this.wrapSelector('#vp_prefixBox textarea')).val();
        if (prefixCode.length > 0) {
            sbCode.appendLine(prefixCode);
        }

        var fontName = $(this.wrapSelector("#vp_slctFontList")).val();
        var fontSize = $(this.wrapSelector("#vp_txtFontSize")).val();

        // 폰트 정보 추가
        sbCode.appendLine("from matplotlib.pylab import rcParams");
        //sbCode.appendLine("rcParams['figure.figsize'] = 12, 8");
        sbCode.appendFormatLine("rcParams['font.family'] = '{0}'", fontName);
        if (fontSize != '')
            sbCode.appendFormatLine("rcParams['font.size'] = {0}", fontSize);

        // cell metadata 작성하기
        // pdGen.vp_setCellMetadata(_VP_CODEMD);

        // add postfix code
        var postfix = $(this.wrapSelector('#vp_postfixBox textarea')).val();
        if (postfix.length > 0) {
            sbCode.appendLine('');
            sbCode.append(postfix);
        }

        if (addCell) this.cellExecute(sbCode.toString(), exec);

        return sbCode.toString();
    }

    return {
        initOption: initOption
    };
});