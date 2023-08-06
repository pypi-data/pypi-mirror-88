define([
    'require'
    , 'jquery'
    , 'notebook/js/mathjaxutils'
    , 'components/marked/lib/marked'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpFuncJS'
    , 'nbextensions/visualpython/src/common/component/vpLineNumberTextArea'
], function (requirejs, $, mathjaxutils, marked, vpCommon, vpConst, sb, vpFuncJS, vpLineNumberTextArea) {
    // 옵션 속성
    const funcOptProp = {
        stepCount : 1
        , funcName : "Markdown"
        , funcID : "com_markdown"
    }

    /**
     * html load 콜백. 고유 id 생성하여 부과하며 js 객체 클래스 생성하여 컨테이너로 전달
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     * @param {JSON} meta 메타 데이터
     */
    var optionLoadCallback = function(callback, meta) {
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
            var mMarkdown = new Markdown(uuid);
            mMarkdown.metadata = meta;
            
            // 옵션 속성 할당.
            mMarkdown.setOptionProp(funcOptProp);
            // html 설정.
            mMarkdown.initHtml();
            callback(mMarkdown);  // 공통 객체를 callback 인자로 전달
        }
    }
    
    /**
     * html 로드. 
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     * @param {JSON} meta 메타 데이터
     */
    var initOption = function(callback, meta) {
        vpCommon.loadHtml(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_GREEN_ROOM)), "markdown/markdown.html", optionLoadCallback, callback, meta);
    }

    /**
     * 본 옵션 처리 위한 클래스
     * @param {String} uuid 고유 id
     */
    var Markdown = function(uuid) {
        this.uuid = uuid;   // Load html 영역의 uuid.
        this.packageList = [
            {}
        ]
        this.package = {
            id: 'com_markdown',
            name: 'Markdown',
            library: 'common',
            description: '마크다운',
            input: [
                {
                    name: vpCommon.formatString("{0}{1}", vpConst.VP_ID_PREFIX, "markdownEditor")
                }
            ]
        }
    }

    /**
     * vpFuncJS 에서 상속
     */
    Markdown.prototype = Object.create(vpFuncJS.VpFuncJS.prototype);

    /**
     * 유효성 검사
     * @returns 유효성 검사 결과. 적합시 true
     */
    Markdown.prototype.optionValidation = function() {
        return true;

        // 부모 클래스 유효성 검사 호출.
        // vpFuncJS.VpFuncJS.prototype.optionValidation.apply(this);
    }

    /**
     * html 내부 binding 처리
     */
    Markdown.prototype.initHtml = function() {
        var sbPageContent = new sb.StringBuilder();

        var lineNumberTextArea = new vpLineNumberTextArea.vpLineNumberTextArea(vpCommon.formatString("{0}{1}", vpConst.VP_ID_PREFIX, "markdownEditor"));
        sbPageContent.appendLine(lineNumberTextArea.toTagString());
        sbPageContent.appendFormatLine("<div class='rendered_html' id='{0}{1}'></div>", vpConst.VP_ID_PREFIX, "markdownPreview");

        this.setPage(sbPageContent.toString());
        $(this.wrapSelector(vpCommon.formatString(".{0}", lineNumberTextArea._UUID))).css({
            width: "calc(100% - 20px)"
            , margin: "10px"
        });
        $(this.wrapSelector("textarea")).css("height", "165px");
        $(this.wrapSelector(vpCommon.formatString("#{0}{1}", vpConst.VP_ID_PREFIX, "markdownPreview"))).css({
            width: "calc(100% - 20px)"
            , margin: "20px 10px 5px 10px"
            , "max-height": "300px"
            , overflow: "auto"
        })
    }

    /**
     * 코드 생성
     * @param {boolean} addCell 셀에 추가
     * @param {boolean} exec 실행여부
     */
    Markdown.prototype.generateCode = function(addCell = false, exec = false) {
        this.generatedCode = $(this.wrapSelector(vpCommon.formatString("#{0}{1}", vpConst.VP_ID_PREFIX, "markdownEditor"))).val();
        if (addCell) {
            this.cellExecute(this.generatedCode, exec, "markdown");
        }

        return this.generatedCode;
    }

    /**
     * 옵션내 이벤트 바인딩.
     */
    Markdown.prototype.bindOptionEvent = function() {
        $(document).on("propertychange change keyup paste input", this.wrapSelector(vpCommon.formatString("#{0}{1}", vpConst.VP_ID_PREFIX, "markdownEditor")), function(evt) {

            previewRender($(this).val());
        });
    }

    var previewRender = function(text) {
        var math = null;
        var text_and_math = mathjaxutils.remove_math(text);
        text = text_and_math[0];
        math = text_and_math[1];

        var renderer = new marked.Renderer();

        marked(text, { renderer: renderer }, function (err, html) {
            html = mathjaxutils.replace_math(html, math);
            document.getElementById(vpCommon.formatString("{0}{1}", vpConst.VP_ID_PREFIX, "markdownPreview")).innerHTML = html;

            MathJax.Hub.Queue(["Typeset", MathJax.Hub, vpCommon.formatString("{0}{1}", vpConst.VP_ID_PREFIX, "markdownPreview")]);
        });
    }

    /**
     * 메타데이터 로드 후 액션
     * @param {funcJS} option
     * @param {JSON} meta 
     */   
    Markdown.prototype.loadMetaExpend = function(funcJS, meta) {
            previewRender($(vpCommon.formatString("#{0}{1}", vpConst.VP_ID_PREFIX, "markdownEditor")).val());
    }

    return {
        initOption: initOption
    };
});
