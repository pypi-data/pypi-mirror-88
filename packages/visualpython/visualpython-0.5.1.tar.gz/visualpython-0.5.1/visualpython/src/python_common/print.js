define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpFuncJS'
    , 'nbextensions/visualpython/src/common/component/vpSuggestInputText'
], function (requirejs, $, vpCommon, vpConst, sb, vpFuncJS, vpSuggestInputText) {
    // 옵션 속성
    const funcOptProp = {
        stepCount : 3
        , funcName : "print()"
        , funcID : "py_print"
        // TODO: 최초에 멀티 옵션 위해 임시 구상했던 부분. 
        // 2020.11.25 현재 불필요. 향후 삭제 예정.
        // , funcArgs : [
        //     { caption : "arg1", type : "number", nullable : false }
        //     , { caption : "arg2", type : Array, nullable : true }
        //     , { caption : "arg3", type : "string", nullable : true }
        // ]
        // , funcRetruns : Array
    }

    /**
     * html load 콜백. 고유 id 생성하여 부과하며 js 객체 클래스 생성하여 컨테이너로 전달
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     * @param {JSON} meta 메타 데이터
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
            var osSample = new PythonCommon(uuid);
            osSample.metadata = meta;
            
            // 옵션 속성 할당.
            osSample.setOptionProp(funcOptProp);

            // html 설정.
            osSample.initHtml();

            // TODO: meta load 처리 방안 검토. 
            // 방안 1. callback 에서 처리
            // 방안 2. initHtml 내에서 meta 존재 시 init과 동시에 처리.
            // 방안 3. initHtml 후에 옵션 내에서 load 함수 호출.

            callback(osSample);  // 객체를 callback 인자로 전달
        }
    }
    
    /**
     * html 로드. 
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     * @param {JSON} meta 메타 데이터
     */
    var initOption = function(callback, meta) {
        vpCommon.loadHtml(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_GREEN_ROOM)), "python_common/index.html", optionLoadCallback, callback, meta);
    }

    /**
     * 본 옵션 처리 위한 클래스
     * @param {String} uuid 고유 id
     */
    var PythonCommon = function(uuid) {
        this.uuid = uuid;   // Load html 영역의 uuid.
        this.state = {

        }
    }

    /**
     * vpFuncJS 에서 상속
     */
    PythonCommon.prototype = Object.create(vpFuncJS.VpFuncJS.prototype);

    /**
     * 유효성 검사
     * @returns 유효성 검사 결과. 적합시 true
     */
    PythonCommon.prototype.optionValidation = function() {
        // FIXME: 해당 옵션 설정이 유효한지 체크.
        // vpContainer.js 에서는 addLibraryToJupyterCell 에서 최초 실행후 return false 인경우 정지하도록 설계함.

        return true;
    }

    /**
     * html 내부 binding 처리
     */
    PythonCommon.prototype.initHtml = function() {
        var sbPageContent = new sb.StringBuilder();
        var sbTagString = new sb.StringBuilder();

        // prefix code 입력 영역
        sbPageContent.appendLine(this.createPrefixCode());
        // sbPageContent.appendLine(this.createManualCode(vpConst.API_OPTION_PREFIX_CAPTION, vpConst.API_OPTION_PREFIX_CODE_ID, vpConst.PREFIX_CODE_SIGNATURE));
        // this.getPrefixCode(); this.setPrefixCode("value"); // prefix code 접근

        // 필수 옵션 테이블 레이아웃
        var tblLayoutRequire = this.createVERSimpleLayout("25%");
        tblLayoutRequire.addClass(vpConst.OPTION_TABLE_LAYOUT_HEAD_HIGHLIGHT);
        var nTmp = 1;

        // // select tag 직접 입력
        // sbTagString.appendLine("<select>");
        // sbTagString.appendLine("<option>one arg</option>");
        // sbTagString.appendFormatLine("<option value='{0}'>{1}</option>", "1", "arg list");
        // sbTagString.appendLine("</select>");
        
        // tblLayoutRequire.addRow("Select", sbTagString.toString());
        
        // // check box 직접 입력, th rowspan type
        // var arrChkRow = new Array();

        // sbTagString.clear();
        // sbTagString.appendLine("<label>");
        // sbTagString.appendFormatLine("<input type='checkbox' {0} />", "checked");
        // sbTagString.appendFormatLine("<span>{0}</span>", "Check box type 1");

        // arrChkRow.push(sbTagString.toString());
        
        // sbTagString.clear();
        // sbTagString.appendFormatLine("<input type='checkbox' {0} id='{1}' />", "checked", "tmpChkBox");
        // sbTagString.appendFormatLine("<label for='{0}'>{1}</label>", "tmpChkBox", "Check box type 2");
        
        // arrChkRow.push(sbTagString.toString());
        // tblLayoutRequire.addRowSpanRow("Checkbox", arrChkRow);

        // // file browser, row insert index
        // sbTagString.clear();
        // sbTagString.appendFormatLine("<input class='{0}' disabled type='text' />", vpConst.FILE_BROWSER_INPUT);
        // sbTagString.appendFormatLine("<div class='{0}'></div>", vpConst.FILE_BROWSER_INPUT_BUTTON);
        
        // tblLayoutRequire.addRow("File Browser", sbTagString.toString(), 1);

        // // radio button TODO: no design. 체크박스와 비슷한 형태로 예상됨.
        // sbTagString.clear();
        // sbTagString.appendLine("<label><input type='radio' checked /><span>Radio</span></label>");

        // tblLayoutRequire.addRow("Radio", sbTagString.toString());

        // // input text
        // sbTagString.clear();
        // sbTagString.appendFormatLine("<input type='text' placeholder='{0}'/>", "Input here");

        // tblLayoutRequire.addRow("Text", sbTagString.toString());

        var suggestInput = new vpSuggestInputText.vpSuggestInputText();
        suggestInput.setComponentID('vp_pyPrint')
        suggestInput.setPlaceholder("Select or input");
        suggestInput.setSuggestList(function() { return ["1","2","3","4","5"]; });
        suggestInput.setNormalFilter(false);
        tblLayoutRequire.addRow("Input Print Data", suggestInput.toTagString());

        // suggestInput = new vpSuggestInputText.vpSuggestInputText();
        // suggestInput.setPlaceholder("Input or select");
        // suggestInput.setComponentID("tmpCompSugg");
        // suggestInput.setSelectEvent(function(selectedValue) { console.log(selectedValue); });
        // var tempSrc = function() {
        //     return ["6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"];
        // };
        // suggestInput.setSuggestList(tempSrc);
        // tblLayoutRequire.addRow("Function Suggest Text", suggestInput.toTagString());

        // tblLayoutRequire.addRow("Modal test", "<button id='modalTest'>Modal Open</button>");
        
        // var that = this;
        // $(document).on("click", "#modalTest", function() {
        //     that.openMultiBtnModal("Modal test", ["Yes", "No", "Cancel"], function(clickIndex) { console.log(clickIndex); });
        // });

        // 필수 옵션 영역 (아코디언 박스)
        var accBoxRequire = this.createOptionContainer(vpConst.API_REQUIRE_OPTION_BOX_CAPTION);
        accBoxRequire.setOpenBox(true);
        accBoxRequire.appendContent(tblLayoutRequire.toTagString());

        sbPageContent.appendLine(accBoxRequire.toTagString());

        // 추가 옵션 테이블 레이아웃
        var tblLayoutAdditional = this.createVERSimpleLayout("30%");

        // tblLayoutAdditional.addRow("Test " + nTmp++ , "<input type='text'/>");
        // tblLayoutAdditional.addRow("Test " + nTmp++ , "<input type='text'/>");
        // tblLayoutAdditional.addRow("Test " + nTmp++ , "<input type='text'/>");
        // tblLayoutAdditional.addRow("Test " + nTmp++ , "<input type='text'/>");

        // 추가 옵션 영역
        var accBoxAdditional = this.createOptionContainer(vpConst.API_ADDITIONAL_OPTION_BOX_CAPTION);
        accBoxAdditional.appendContent(tblLayoutAdditional.toTagString());

        sbPageContent.appendLine(accBoxAdditional.toTagString());

        // this.setPage(sbPageContent.toString());

        // sbPageContent.clear();

        // // 테이블 레이아웃등 개발 테스트
        // tblLayoutAdditional = this.createHORIZSimpleLayout();
        // tblLayoutAdditional.setMergeCellClass(vpConst.TABLE_LAYOUT_CELL_CENTER_ALIGN);
        // tblLayoutAdditional.setHeaderCellCenterAlign(false);

        // tblLayoutAdditional.setColWidth(["100px", "100px", "", , "100px"]);
        // tblLayoutAdditional.setHeader(["Colum 1", "Colum 2", "Colum 3", tblLayoutAdditional.MERGED_CELL, "Colum 4"]);
        // tblLayoutAdditional.addRow(["Data 1", tblLayoutAdditional.MERGED_CELL, tblLayoutAdditional.MERGED_CELL, "Data 2", "Data 3"]);
        // tblLayoutAdditional.addRow(["Data 1", tblLayoutAdditional.MERGED_CELL, tblLayoutAdditional.MERGED_CELL, tblLayoutAdditional.MERGED_CELL, tblLayoutAdditional.MERGED_CELL]);
        // tblLayoutAdditional.addRow(["Data 1", "Data 2", "Data 3", "Data 4", "Data 5"], 0);
        
        // accBoxAdditional = this.createOptionContainer("Test Layout and others");
        // accBoxAdditional.appendContent(tblLayoutAdditional.toTagString());

        // sbPageContent.appendLine(accBoxAdditional.toTagString());

        // postfix code 입력 영역
        sbPageContent.appendLine(this.createPostfixCode());
        // sbPageContent.appendLine(this.createManualCode(vpConst.API_OPTION_POSTFIX_CAPTION, vpConst.API_OPTION_POSTFIX_CODE_ID));
        // this.getPostfixCode(); this.setPostfixCode("value"); // postefix code 접근

        
        this.setPage(sbPageContent.toString());
        sbPageContent.clear();
    }

    /**
     * 코드 생성
     * @param {boolean} addCell 셀에 추가
     * @param {boolean} exec 실행여부
     * @returns 생성된 코드
     */
    PythonCommon.prototype.generateCode = function(addCell = false, exec = false) {
        // TODO: code 생성하여 실행 처리
        var code = $(this.wrapSelector('#vp_prefixCodeArea')).val() + ' - ' + 'python' + ' > ' + 'Built-in functions'+ ' > ' + 'print()' + '\n';
        code += 'print' + '('+$(this.wrapSelector('#vp_pyPrint')).val() +')'+ '\n';
        code +=  $(this.wrapSelector('#vp_postfixCodeArea')).val();

        this.cellExecute(code, exec);
    }

    return {
        initOption: initOption
    };
});
