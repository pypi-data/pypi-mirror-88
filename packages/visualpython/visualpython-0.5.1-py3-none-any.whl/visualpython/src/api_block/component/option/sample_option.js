define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/component/vpSuggestInputText'
    , '../../api.js'    
    , '../../config.js'
    , '../../constData.js'
    , '../../blockRenderer.js'
    
], function ( $, vpCommon, vpConst, sb, vpSuggestInputText, api, config, constData, blockRenderer ) {
    const { ChangeOldToNewState
        , FindStateValue

        , CreateOneArrayValueAndGet
        , UpdateOneArrayValueAndGet
        , DeleteOneArrayValueAndGet

        , DestructureFromBlockArray

        , MakeFirstCharToUpperCase
        , MapTypeToName
        , RemoveSomeBlockAndGetBlockList
        , ShuffleArray
        , GetImageUrl
        , ControlToggleInput } = api;

    const { PROCESS_MODE } = config;

    const { } = blockRenderer;

    const { BLOCK_DIRECTION
            , BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , STR_COLON_SELECTED
            , STR_NULL
            , STR_FOR
            , STR_INPUT
            , STR_CHANGE_KEYUP_PASTE

            , STATE_returnOutParamList } = constData;


    var InitSampleBlockOption = function(thatBlock, optionPageSelector) {
        var uuid = thatBlock.getUUID();
        var blockContainerThis = thatBlock.getBlockContainerThis();
        var importPackageThis = blockContainerThis.getImportPackageThis();
        // var blockOptionContainer = importPackageThis.createOptionContainer();


        var sbPageContent = new sb.StringBuilder();
        var sbTagString = new sb.StringBuilder();

        // prefix code 입력 영역
        sbPageContent.appendLine(importPackageThis.createPrefixCode());
        // sbPageContent.appendLine(this.createManualCode(vpConst.API_OPTION_PREFIX_CAPTION, vpConst.API_OPTION_PREFIX_CODE_ID, vpConst.PREFIX_CODE_SIGNATURE));
        // this.getPrefixCode(); this.setPrefixCode("value"); // prefix code 접근

        // 필수 옵션 테이블 레이아웃
        var tblLayoutRequire = importPackageThis.createVERSimpleLayout("25%");
        tblLayoutRequire.addClass(vpConst.OPTION_TABLE_LAYOUT_HEAD_HIGHLIGHT);
        var nTmp = 1;

        // select tag 직접 입력
        sbTagString.appendLine("<select>");
        sbTagString.appendLine("<option>Select</option>");
        sbTagString.appendFormatLine("<option value='{0}'>{1}</option>", "1", "option 1");
        sbTagString.appendFormatLine("<option value='{0}'>{1}</option>", "2", "option 2");
        sbTagString.appendFormatLine("<option value='{0}'>{1}</option>", "3", "option 3");
        sbTagString.appendFormatLine("<option value='{0}'>{1}</option>", "4", "option 4");
        sbTagString.appendLine("</select>");
        
        tblLayoutRequire.addRow("Select", sbTagString.toString());
        
        // check box 직접 입력, th rowspan type
        var arrChkRow = new Array();

        sbTagString.clear();
        sbTagString.appendLine("<label>");
        sbTagString.appendFormatLine("<input type='checkbox' {0} />", "checked");
        sbTagString.appendFormatLine("<span>{0}</span>", "Check box type 1");

        arrChkRow.push(sbTagString.toString());
        
        sbTagString.clear();
        sbTagString.appendFormatLine("<input type='checkbox' {0} id='{1}' />", "checked", "tmpChkBox");
        sbTagString.appendFormatLine("<label for='{0}'>{1}</label>", "tmpChkBox", "Check box type 2");
        
        arrChkRow.push(sbTagString.toString());
        tblLayoutRequire.addRowSpanRow("Checkbox", arrChkRow);

        // file browser, row insert index
        sbTagString.clear();
        sbTagString.appendFormatLine("<input class='{0}' disabled type='text' />", vpConst.FILE_BROWSER_INPUT);
        sbTagString.appendFormatLine("<div class='{0}'></div>", vpConst.FILE_BROWSER_INPUT_BUTTON);
        
        tblLayoutRequire.addRow("File Browser", sbTagString.toString(), 1);

        // radio button TODO: no design. 체크박스와 비슷한 형태로 예상됨.
        sbTagString.clear();
        sbTagString.appendLine("<label><input type='radio' checked /><span>Radio</span></label>");

        tblLayoutRequire.addRow("Radio", sbTagString.toString());

        // input text
        sbTagString.clear();
        sbTagString.appendFormatLine("<input type='text' placeholder='{0}'/>", "Input here");

        tblLayoutRequire.addRow("Text", sbTagString.toString());

        var suggestInput = new vpSuggestInputText.vpSuggestInputText();
        suggestInput.setPlaceholder("Select or input");
        suggestInput.setSuggestList(["1","2","3","4","5"]);
        tblLayoutRequire.addRow("Suggest Text", suggestInput.toTagString());

        suggestInput = new vpSuggestInputText.vpSuggestInputText();
        suggestInput.setPlaceholder("Input or select");
        suggestInput.setComponentID("tmpCompSugg");
        var tempSrc = function() {
            return ["6","7","8","9","10"];
        };
        suggestInput.setSuggestList(tempSrc);
        tblLayoutRequire.addRow("Function Suggest Text", suggestInput.toTagString());

        var suggestInput_jycustom = new vpSuggestInputText.vpSuggestInputText();
        suggestInput_jycustom.setPlaceholder("Auto complete");
        suggestInput_jycustom.setSuggestList(["x0","x1","x2","x3","x4"]);
        suggestInput_jycustom.setComponentID('vp_autocompleteJy');

        var suggestInput_jycustomStr = suggestInput_jycustom.toTagString();
        tblLayoutRequire.addRow("autocomplete", suggestInput_jycustomStr);
        // show api list
        $(document).on('click', vpCommon.wrapSelector(`#vp_autocompleteJy`), function(event) {
            console.log('$(this).val()', $(this).val(), event);
        });
        
        // $(document).on('change', vpCommon.wrapSelector(`#vp_autocompleteJy`), function(event) {
        //     console.log('event', event);
        // });

        // $(document).on('propertychange', vpCommon.wrapSelector(`#vp_autocompleteJy`), function(event) {
        //     console.log('propertychange event', event);
        // });

        // $(document).on('select', vpCommon.wrapSelector(`#vp_autocompleteJy`), function(event) {
        //     console.log('select event', event);
        // });



        // $(document).on('autocomplete', vpCommon.wrapSelector(`#vp_autocompleteJy`), function(event) {
        //     console.log('autocomplete event', event);
        // });


        // $(document).on('focus', vpCommon.wrapSelector(`#vp_autocompleteJy`), function(event) {
        //     console.log('focus event', event);
        // });



    

        // $(vpCommon.wrapSelector('#vp_autocompleteJy')).autocomplete('option', 'source', ["x5","x6","x7","x8","x9"]);
        // $(vpCommon.wrapSelector('#vp_autocompleteJy'))('option', 'source', []);
        // $(vpCommon.wrapSelector('#vp_autocompleteJy')).autocomplete({
        //     source: ["x0","x1","x2","x3","x4"],
        //     minLength: 2,
        //     autoFocus: true,
        //     select: function(event, ui) {
        //         console.log('ui', ui);
        //         // $(that.wrapSelector('#vp_varApiSearch')).val(ui.item.value);
        //         // $(that.wrapSelector('#vp_varApiFuncId')).val(ui.item.id);

        //         // that.replaceBoard();
        //     },
        //     change: function(event, ui) {
        //         console.log('ui', ui);
        //         // that.replaceBoard();
        //     }
        // });
        // var suggestInput_jycustomStr = suggestInput_jycustom.toTagString();
        // tblLayoutRequire.addRow("autocomplete", suggestInput_jycustomStr);
        // var count = 0;
        // $(suggestInput_jycustomStr).click(function() {
        //     var newid = "cloned_" + (count++); // Generates a unique id
        //     var clone = $(source) // the input with autocomplete your want to clone
        //         .clone()
        //         .attr("id",newid) // Must give a new id with clone
        //         .val("") // Clear the value (optional)
        //         .appendTo(target);
        //     console.log('clone',clone);
        // });

        // 필수 옵션 영역 (아코디언 박스)
        var accBoxRequire = importPackageThis.createOptionContainer(vpConst.API_REQUIRE_OPTION_BOX_CAPTION);
        accBoxRequire.setOpenBox(importPackageThis);
        accBoxRequire.appendContent(tblLayoutRequire.toTagString());

        sbPageContent.appendLine(accBoxRequire.toTagString());

        // $(optionPageSelector).append(sbPageContent.toString());

        // 추가 옵션 테이블 레이아웃
        var tblLayoutAdditional = importPackageThis.createVERSimpleLayout("30%");

        tblLayoutAdditional.addRow("Test " + nTmp++ , "<input type='text'/>");
        tblLayoutAdditional.addRow("Test " + nTmp++ , "<input type='text'/>");
        tblLayoutAdditional.addRow("Test " + nTmp++ , "<input type='text'/>");
        tblLayoutAdditional.addRow("Test " + nTmp++ , "<input type='text'/>");

        // 추가 옵션 영역
        var accBoxAdditional = importPackageThis.createOptionContainer(vpConst.API_ADDITIONAL_OPTION_BOX_CAPTION);
        accBoxAdditional.appendContent(tblLayoutAdditional.toTagString());

        sbPageContent.appendLine(accBoxAdditional.toTagString());
        $(optionPageSelector).append(sbPageContent.toString());
        // importPackageThis.setPage(sbPageContent.toString());

        sbPageContent.clear();
        {


            // 테이블 레이아웃등 개발 테스트
            tblLayoutAdditional = importPackageThis.createHORIZSimpleLayout();
            tblLayoutAdditional.setMergeCellClass(vpConst.TABLE_LAYOUT_CELL_CENTER_ALIGN);
            tblLayoutAdditional.setHeaderCellCenterAlign(false);

            tblLayoutAdditional.setColWidth(["100px", "100px", "", , "100px"]);
            tblLayoutAdditional.setHeader(["Colum 1", "Colum 2", "Colum 3", tblLayoutAdditional.MERGED_CELL, "Colum 4"]);
            tblLayoutAdditional.addRow(["Data 1", tblLayoutAdditional.MERGED_CELL, tblLayoutAdditional.MERGED_CELL, "Data 2", "Data 3"]);
            tblLayoutAdditional.addRow(["Data 1", tblLayoutAdditional.MERGED_CELL, tblLayoutAdditional.MERGED_CELL, tblLayoutAdditional.MERGED_CELL, tblLayoutAdditional.MERGED_CELL]);
            tblLayoutAdditional.addRow(["Data 1", "Data 2", "Data 3", "Data 4", "Data 5"], 0);
            
            accBoxAdditional = importPackageThis.createOptionContainer("Test Layout and others");
            accBoxAdditional.appendContent(tblLayoutAdditional.toTagString());

            sbPageContent.appendLine(accBoxAdditional.toTagString());

            // postfix code 입력 영역
            sbPageContent.appendLine(importPackageThis.createPostfixCode());
        // sbPageContent.appendLine(this.createManualCode(vpConst.API_OPTION_POSTFIX_CAPTION, vpConst.API_OPTION_POSTFIX_CODE_ID));
        // this.getPostfixCode(); this.setPostfixCode("value"); // postefix code 접근

        }


        // importPackageThis.setPage(sbPageContent.toString(), 1);

        // $(optionPageSelector).append(sbPageContent.toString());
    }
    return InitSampleBlockOption;
});