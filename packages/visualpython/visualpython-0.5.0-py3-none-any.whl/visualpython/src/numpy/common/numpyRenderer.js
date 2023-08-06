define ([
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/vpMakeDom'
    , 'nbextensions/visualpython/src/common/StringBuilder'

    // + 추가 numpy 폴더  패키지 : 이진용 주임
    , 'nbextensions/visualpython/src/numpy/api/numpyStateApi' 
    , 'nbextensions/visualpython/src/numpy/constData'
], function( vpCommon, vpMakeDom, sb, numpyStateApi, constData ) {
    const { STR_CHANGE_KEYUP_PASTE } = constData;
    const { updateOneArrayIndexValueAndGetNewArray: updateOneArrayValueAndGet, 
            deleteOneArrayIndexValueAndGetNewArray: deleteOneArrayValueAndGet } = numpyStateApi;
    const { renderDiv, renderInput, renderButton, renderSpan } = vpMakeDom;

    var NumpyRenderer = function(numpyOptionObj) {
        const { numpyDtypeArray, numpyIndexValueArray, numpyEnumRenderEditorFuncType } = numpyOptionObj;
        this.numpyDtypeArray = numpyDtypeArray;
        this.numpyIndexValueArray = numpyIndexValueArray;
        this.numpyEnumRenderEditorFuncType = numpyEnumRenderEditorFuncType;

        /** setImportPackageThis 메소드로 동적 set */
        this.importPackageThis;

        /** 배열을 동적으로 추가 삭제 생성할 때마다 값이 달라진다 */
        this.oneArrayLength = 0;

        this.twoArrayRow = 0;
        this.twoArrayCol = 0;

        this.threeArrayRow = 0;
        this.threeArrayCol = 0;
        this.threeArrayDepth = 0;

        /** mainPageSelector는 numpy의 첫번째 페이지의 <div> css class selector
            optionPageSelector는 numpy의 두번째 페이지의 <div> css class selector*/
        this.mainPageSelector = `.vp-numpy-mainPageBlock-view`;
        this.requiredPageSelector = `.vp-numpy-requiredPageBlock-view`;
        this.optionPageSelector = `.vp-numpy-optionPageBlock-view`;
        this.rootTagSelector = ``;

        this.numpyState = null;

        this.funcName = ``;
    };

    /**
    * pageList index.js 파일에서 importPackage 인스턴스의 this를 가져오는 메소드
    * @param {ImportPackage Instance this} importPackageThis 
    */
    NumpyPageRender.prototype.setImportPackageThis = function(importPackageThis) {
        this.importPackageThis = importPackageThis;
    }
    NumpyPageRender.prototype.getImportPackageThis = function() {
        return this.importPackageThis;
    }

    NumpyRenderer.prototype.setNumpyState = function(numpyState) {
        this.numpyState = numpyState;
    }
    NumpyRenderer.prototype.getNumpyState = function() {
        return this.numpyState;
    }

    NumpyPageRender.prototype.setMainPageSelector = function(mainPageSelector) {
        this.mainPageSelector = mainPageSelector;
    }
    NumpyPageRender.prototype.getMainPageSelector = function() {
        return this.mainPageSelector;
    }

    NumpyPageRender.prototype.setOptionPageSelector = function(optionPageSelector) {
        this.optionPageSelector = optionPageSelector;
    }
    NumpyPageRender.prototype.getOptionPageSelector = function() {
        return this.optionPageSelector;
    }

    NumpyPageRender.prototype.setRequiredPageSelector = function(requiredPageSelector) {
        this.requiredPageSelector = requiredPageSelector;
    }
    NumpyPageRender.prototype.getRequiredPageSelector = function() {
        return this.requiredPageSelector;
    }

    NumpyPageRender.prototype.setRootTagSelector = function(rootTagSelector) {
        this.rootTagSelector = rootTagSelector;
    }
    NumpyPageRender.prototype.getRootTagSelector = function() {
        return this.rootTagSelector;
    }

    /**
     * NumpyPageRender 클래스의 pageRender 메소드 오버라이드
     */
    NumpyRenderer.prototype.render = function(tagSelector) {

    }

    NumpyRenderer.prototype.renderAdditionalOptionContainer = function() {
        var importPackageThis = this.getImportPackageThis();
        var rootTagSelector = this.getRootTagSelector();
        var optionPage = $(importPackageThis.wrapSelector(rootTagSelector));

        var sbTagString = new sb.StringBuilder();
        sbTagString.appendFormatLine("<div class='{0} {1} {2}' >", 'vp-numpy-optionPageBlock-view', 'vp-numpy-block', 'vp-minimize' );
        sbTagString.appendLine("<h4>");
        sbTagString.appendFormatLine("<div class='{0} {1}' >", 'vp-panel-area-vertical-btn', 'vp-arrow-down');
        sbTagString.appendLine("</div>");
        sbTagString.appendFormatLine("<span class='{0}' data-caption-id='{1}'>", 'vp-multilang', 'Variable');
        sbTagString.appendFormatLine("{0}", 'Additional Options');
        sbTagString.appendLine("</span>");
        sbTagString.appendLine("</h4>");
        sbTagString.appendLine("</div>");

        var additionalOptionDom = $(sbTagString.toString());  
        optionPage.append(additionalOptionDom);
    }

    NumpyRenderer.prototype.renderPostfixCode = function() {
        var importPackageThis = this.getImportPackageThis();
        var numpyState = this.getNumpyState();
        var rootTagSelector = this.getRootTagSelector();
        var mainPage = $(importPackageThis.wrapSelector(rootTagSelector));

        var sbTagString = new sb.StringBuilder();
        sbTagString.appendFormatLine("<div class='{0} {1} {2}' >", 'vp-numpy-block', 'vp-user-option-box', 'vp-minimize' );
        sbTagString.appendLine("<h4>");
        sbTagString.appendFormatLine("<div class='{0} {1}' >", 'vp-panel-area-vertical-btn', 'vp-arrow-down');
        sbTagString.appendLine("</div>");
        sbTagString.appendFormatLine("<span class='{0}' data-caption-id='{1}'>", 'vp-multilang', 'Variable');
        sbTagString.appendFormatLine("{0}", 'Postfix Code');
        sbTagString.appendLine("</span>");
        sbTagString.appendLine("</h4>");
        sbTagString.appendFormatLine("<div id='{0}'>", 'vp_postfixBox');
        sbTagString.appendFormatLine("<textarea class='{0} {1}' placeholder='{2}' rows='3' cols='60'>", 
                                'vp-numpy-textarea', 'vp-numpy-postfix-textarea', 'postfix code');
        sbTagString.appendLine("</textarea>");
        sbTagString.appendLine("</div>");
        sbTagString.appendLine("</div>");

        var postfixCodeDom = $(sbTagString.toString());    
        mainPage.append(postfixCodeDom);

        mainPage.on('focus', '.vp-numpy-postfix-textarea', function() {
            Jupyter.notebook.keyboard_manager.disable();
        });
        mainPage.on('blur', '.vp-numpy-postfix-textarea', function() {
            Jupyter.notebook.keyboard_manager.enable();
        });

        /** postfix Code */
        $(importPackageThis.wrapSelector(`.vp-numpy-postfix-textarea`)).on(STR_CHANGE_KEYUP_PASTE, function() {
            numpyState.setState({
                postfixCode: $(this).val()
            });
        });
    }

    NumpyRenderer.prototype.renderPrefixCode = function() {
        var importPackageThis = this.getImportPackageThis();
        var numpyState = this.getNumpyState();
        var rootTagSelector = this.getRootTagSelector();
        var mainPage = $(importPackageThis.wrapSelector(rootTagSelector));

        var sbTagString = new sb.StringBuilder();
        sbTagString.appendFormatLine("<div class='{0} {1} {2}' >", 'vp-numpy-block', 'vp-user-option-box', 'vp-minimize' );
        sbTagString.appendLine("<h4>");
        sbTagString.appendFormatLine("<div class='{0} {1}' ></div>", 'vp-panel-area-vertical-btn', 'vp-arrow-down' );
        sbTagString.appendFormatLine("<span class='{0}' data-caption-id='{1}'>", 'vp-multilang', 'Variable');
        sbTagString.appendFormatLine("{0}", 'Prefix Code');
        sbTagString.appendLine("</span>");
        sbTagString.appendLine("</h4>");
        sbTagString.appendFormatLine("<div id='{0}'>", 'vp_prefixBox');
        sbTagString.appendFormatLine("<textarea class='{0} {1}' placeholder='{2}' rows='3' cols='60'>", 
                                                'vp-numpy-textarea', 'vp-numpy-prefix-textarea', 'prefix code');
        sbTagString.appendLine("</textarea>");
        sbTagString.appendLine("</div>");
        sbTagString.appendLine("</div>");
        var prefixDom = $(sbTagString.toString());  

        var mainPage = $(importPackageThis.wrapSelector(rootTagSelector));
        mainPage.append(prefixDom);

        mainPage.on('focus', '.vp-numpy-prefix-textarea', function() {
            Jupyter.notebook.keyboard_manager.disable();
        });
        mainPage.on('blur', '.vp-numpy-prefix-textarea', function() {
            Jupyter.notebook.keyboard_manager.enable();
        });    

        /** prefix Code */
        $(importPackageThis.wrapSelector(`.vp-numpy-prefix-textarea`)).on(STR_CHANGE_KEYUP_PASTE, function() {
            numpyState.setState({
                prefixCode: $(this).val()
            });
        });
    }

    NumpyRenderer.prototype.renderUserOption = function() {
        var uuid = vpCommon.getUUID();
  
        var importPackageThis = this.getImportPackageThis();
        var numpyState = this.getNumpyState();

        var rootTagSelector = this.getRootTagSelector();
        var mainPage = $(importPackageThis.wrapSelector(rootTagSelector));

        var sbTagString = new sb.StringBuilder();
        sbTagString.appendFormatLine("<div class='{0} {1} {2}' >", 'vp-numpy-block', 'vp-numpy-useroption', 'vp-minimize' );
        sbTagString.appendLine("<h4>");
        sbTagString.appendFormatLine("<div class='{0} {1} ' ></div>", 'vp-panel-area-vertical-btn', 'vp-arrow-down' );
        sbTagString.appendFormatLine("<span class='{0}' data-caption-id='{1}'>", 'vp-multilang', 'Variable');
        sbTagString.appendFormatLine("{0}", 'User Option');
        sbTagString.appendLine("</span>");
        sbTagString.appendLine("</h4>");
        sbTagString.appendFormatLine("<div id='{0}' class='{1}' >", 'vp_userOption', 'vp-list-container');
        sbTagString.appendFormatLine("<table class='{0} {1}' style='width:100%;'>", 
                                            'vp-tbl-search-result', 'vp-numpy-useroption-table');
        sbTagString.appendLine("</table>");
        sbTagString.appendLine("</div>");
        sbTagString.appendLine("</div>");
        var userOptionDom = $(sbTagString.toString());  
        mainPage.append(userOptionDom);    
        
        this.renderUserOptionList();
    }

    NumpyRenderer.prototype.renderUserOptionList = function() {
        var numpyState = this.getNumpyState();
        var userOptionTable = $('.vp-numpy-useroption-table');
        $(userOptionTable).empty();

        var colgroup = null;
        {
            var sbTagString = new sb.StringBuilder();
            sbTagString.appendLine("<colgroup>");
            sbTagString.appendLine("<col width='40%'/>");
            sbTagString.appendLine("<col width='*'/>");
            sbTagString.appendLine("<col width='10%'/>");
            sbTagString.appendLine("</colgroup>");
            colgroup = $(sbTagString.toString());  
        }

        var userOptionTableHeader = null;
        {
            var sbTagString = new sb.StringBuilder();
            sbTagString.appendLine("<tr>");
            sbTagString.appendLine("<th>옵션 키</th>");
            sbTagString.appendLine("<th>옵션 값</th>");
            sbTagString.appendLine("<th>X</th>");
            sbTagString.appendLine("</tr>");
            userOptionTableHeader = $(sbTagString.toString());  
        }

        userOptionTable.append(colgroup);     
        userOptionTable.append(userOptionTableHeader);     
        for (var i = 0; i < numpyState.getState('userOptionList').length; i++) {
            (function(j) {
                var optionKey = numpyState.getState('userOptionList')[j].optionKey;
                var optionValue = numpyState.getState('userOptionList')[j].optionValue;

                var sbTagString = new sb.StringBuilder();
                sbTagString.appendFormatLine("<tr class='{0}' >", `vp-numpy-useroption-element-${j}-${uuid}`);
                sbTagString.appendLine("<td>");
                sbTagString.appendFormatLine("<input class='{0} {1}' style='width: 100%;' value='{2}' type='text' >", 
                                                    'vp-numpy-input', `vp-numpy-useroption-key-${j}-${uuid}`, optionKey);
                sbTagString.appendLine("</td>");

                sbTagString.appendLine("<td>");
                sbTagString.appendFormatLine("<input class='{0} {1}' style='width: 100%;' value='{2}' type='text' >", 
                                                    'vp-numpy-input', `vp-numpy-useroption-value-${j}-${uuid}`, optionValue);
                sbTagString.appendLine("</td>");

                sbTagString.appendLine("<td>");
                sbTagString.appendFormatLine("<input class='{0} {1}' type='button'  value='X' >", 
                                                     `vp-numpy-useroption-deleteBtn-${j}-${uuid}`, `vp-numpy-func_btn`);
                sbTagString.appendLine("</td>");
                var userOptionBlock = $(sbTagString.toString());  
     
                userOptionTable.append(userOptionBlock);


                /**
                 *   값 변경
                 */
                $(importPackageThis.wrapSelector(`.vp-numpy-useroption-key-${j}-${uuid}`)).on(STR_CHANGE_KEYUP_PASTE, function() {
                    var updatedIndexValue = $(importPackageThis.wrapSelector(`.vp-numpy-useroption-key-${j}-${uuid}`)).val();
                    numpyState.getState('userOptionList')[j].optionKey = updatedIndexValue;
                });

                $(importPackageThis.wrapSelector(`.vp-numpy-useroption-value-${j}-${uuid}`)).on(STR_CHANGE_KEYUP_PASTE, function() {
                    var updatedIndexValue = $(importPackageThis.wrapSelector(`.vp-numpy-useroption-value-${j}-${uuid}`)).val();
                    numpyState.getState('userOptionList')[j].optionValue = updatedIndexValue;
                });

                /**
                 *  값 삭제
                 */
                $(importPackageThis.wrapSelector(`.vp-numpy-useroption-deleteBtn-${j}-${uuid}`)).click(function() {
                    var deletedParamOneArray = deleteOneArrayIndexValueAndGetNewArray(numpyState.getState('userOptionList'),j);
    
                    numpyState.setState({
                        userOptionList: deletedParamOneArray
                    });
    
                    renderUserOptionList();
                });
            })(i);
        }

        var userOptionButton = null;
        {
            var sbTagString = new sb.StringBuilder();
            sbTagString.appendLine("<tr>");
            sbTagString.appendLine("<td colspan='3'>");
            sbTagString.appendFormatLine("<input class='{0} {1} {2}' type='button' id='vp_addOption' style='width:100%;' value='plus option'>", 
                                            'vp-numpy-useroption-plus-btn', 'vp-numpy-func_btn', 'vp-numpy-padding-1rem');
            sbTagString.appendLine("</td>");
            sbTagString.appendLine("</tr>");
            userOptionButton = $(sbTagString.toString());  
        }

        userOptionTable.append(userOptionButton);

        /** 값 생성*/
        $('.vp-numpy-useroption-plus-btn').click(function() {
            var newData = {
                optionKey: ''
                , optionValue: ''
            }
            numpyState.setState({
                userOptionList: [...numpyState.getState('userOptionList'), newData]
            });

            renderUserOptionList();    
        });
    }
    /**
     * dtype block 생성
     * @returns html accordion box tag string
     */
    NumpyRenderer.prototype.renderDtypeBlock = function() {
        var uuid = vpCommon.getUUID();
        
        var numpyState = this.getNumpyState();
        var importPackageThis = this.getImportPackageThis();
        var optionPageSelector = this.getOptionPageSelector();
        var optionPage = $(importPackageThis.wrapSelector(optionPageSelector));
       
        var numpyDtypeArray = this.numpyDtypeArray;
        var sbTagString = new sb.StringBuilder();

        sbTagString.appendFormatLine("<div class='{0} {1} {2}' ", 'vp-numpy-option-block', 'vp-spread', 'vp-numpy-style-flex-row' );
        sbTagString.appendFormatLine("     style='{0}' >", 'padding-top: 10px' );
        sbTagString.appendFormatLine("<table style='{0}' >", 'width: 100%' );
        sbTagString.appendLine("<tr>" );
        sbTagString.appendLine("<td style='width: 40%;'>" );
        sbTagString.appendLine("<label class='vp-multilang' data-caption-id='selectDtype'>" );
        sbTagString.appendFormatLine("{0}", 'Select Dtype');
        sbTagString.appendLine("</label>" );
        sbTagString.appendLine("</td>" );
        sbTagString.appendLine("<td>" );
        sbTagString.appendFormatLine("<select class='vp-numpy-select-dtype' id='{0}'>", `vp_numpyDtype-${uuid}` );
        sbTagString.appendLine("</select>" );
        sbTagString.appendLine("</td>" );
        sbTagString.appendLine("</tr>" );
        sbTagString.appendLine("</table>" );
        sbTagString.appendLine("</div>" );

        var dtypeBlock = $(sbTagString.toString());            
        optionPage.append(dtypeBlock);

        numpyDtypeArray.forEach(function (element) {
            $(importPackageThis.wrapSelector(`#vp_numpyDtype-${uuid}`)).append(`<option value='${element.value}'> ${element.name}</option>`)
        });

        /** dtype 선택  이벤트 함수 */
        $(importPackageThis.wrapSelector(`#vp_numpyDtype-${uuid}`)).change(function()  {
            numpyState.setState({
                dtype: $(':selected', this).val()
            });
        });
    }

    NumpyRenderer.prototype.renderReturnVarBlock = function() {
        var uuid = vpCommon.getUUID();
 
        var sbTagString = new sb.StringBuilder();
        sbTagString.appendFormatLine("<div class='{0} {1}' id='{2}' style='padding-top: 10px;'>", 
                                        'vp-numpy-option-block', 'vp-spread', 'vp_blockArea');
        sbTagString.appendLine("<table style='width: 100%;'>" );
        sbTagString.appendLine("<tr>" );
        sbTagString.appendLine("<td style='width: 40%;'>" );
        sbTagString.appendFormatLine("<label class='{0}' data-caption-id='{1}' style='margin-bottom: 0px;'> ",
                                             'vp-multilang', 'inputReturnVariable');
        sbTagString.appendFormatLine("{0}", 'Input Return Variable');
        sbTagString.appendLine("</label>" );
        sbTagString.appendLine("</td>" );
        sbTagString.appendLine("<td>" );
        sbTagString.appendFormatLine("<input type='text' class='{0} {1}' id='{2}' placeholder='{3}'/>", 
                                            'vp-numpy-input', 'vp-numpy-return-input', `vp_numpyReturnVarInput-${uuid}`, 'input variable');
        sbTagString.appendLine("</td>" );
        sbTagString.appendLine("</tr>" );
        sbTagString.appendLine("</table>" );
        sbTagString.appendLine("</div>" );

        var returnVarBlock = $(sbTagString.toString()); 
        var importPackageThis = this.getImportPackageThis();
        var numpyState = this.getNumpyState();

        var optionPageSelector = this.getOptionPageSelector();
        var optionPage = $(importPackageThis.wrapSelector(optionPageSelector));
        optionPage.append(returnVarBlock);

        /** return 변수 입력 */
        $(importPackageThis.wrapSelector(`#vp_numpyReturnVarInput-${uuid}`)).on(STR_CHANGE_KEYUP_PASTE, function() {
            numpyState.setState({
                returnVariable: $(this).val()
            });
        });

        // return 변수 print 여부 선택
        $(importPackageThis.wrapSelector(`#vp_numpyInputCheckBox-${uuid}`)).click(function() {
            numpyState.setState({
                isReturnVariable: $(this).is(':checked')
            });
        });    
    }

    NumpyRenderer.prototype.renderCallVarBlock = function() {
        var uuid = vpCommon.getUUID();
        var importPackageThis = this.getImportPackageThis();
        var numpyState = this.getNumpyState();
 
        var sbTagString = new sb.StringBuilder();
        sbTagString.appendFormatLine("<div class='{0} {1}' id='{2}' style='padding-top: 10px;'>", 
                                           'vp-numpy-option-block', 'vp-spread', 'vp_blockArea');
        sbTagString.appendLine("<table style='width: 100%;'>" );        
        sbTagString.appendLine("<tr>" );
        sbTagString.appendLine("<td style='width: 40%;'>" );
        sbTagString.appendFormatLine("<label class='{0}' data-caption-id='{1}' style='margin-bottom: 0px;'> ",
                                            'vp-multilang', 'inputReturnVariable');
        sbTagString.appendFormatLine("{0}", '* Input Call Variable');
        sbTagString.appendLine("</label>" );
        sbTagString.appendLine("</td>" );
        sbTagString.appendLine("<td>" );
        sbTagString.appendFormatLine("<input type='text' class='{0} {1}' id='{2}' placeholder='{3}'/>", 
                                            'vp-numpy-input', 'vp-numpy-callVar-input', `vp_numpyCallVarInput-${uuid}`, 'input variable');
        sbTagString.appendLine("</td>" );
        sbTagString.appendLine("</tr>" );
        sbTagString.appendLine("</table>" );
        sbTagString.appendLine("</div>" );
        
        var callVarBlock = $(sbTagString.toString()); 
        var requiredTagSelector = this.getRequiredPageSelector();
        var requiredPage = $(importPackageThis.wrapSelector(requiredTagSelector));
        requiredPage.append(callVarBlock);

        /** call 변수 입력 */
        $(importPackageThis.wrapSelector(`#vp_numpyCallVarInput-${uuid}`)).on(STR_CHANGE_KEYUP_PASTE, function() {
            numpyState.setState({
                callVariable: $(this).val()
            });
        });
    }

    NumpyRenderer.prototype.resetArrayEditor = function(baseDom) {
        // 동적 랜더링할 태그에 css flex-column 설정
        baseDom.css('display','flex');
        baseDom.css('flexDirection','column');
        // 기존의 렌더링 태그들 리셋하고 아래 로직에서 다시 그림
        baseDom.empty()
    }

    NumpyRenderer.prototype.renderParamArrayEditorTitle = function(baseDom, tagSelector, stateParamName, funcId) {
        var that = this;
        var importPackageThis = this.getImportPackageThis();
        var numpyState = this.getNumpyState();
        var uuid = vpCommon.getUUID();
        var dom = null;

        switch(funcId){
            /**
             * oneArrayEditor
             */
            case 'JY901':{
                /** 1차원 배열 행의 길이를 구하는 로직 */
                this.setOneArrayLength ( numpyState.getState(stateParamName).length );
                            
                /** 1차원 배열 길이 값 입력 <div>블럭 생성 */
        
                {
                    var sbTagString = new sb.StringBuilder();
                    sbTagString.appendFormatLine("<div class='{0}' style='margin-bottom:5px;'>", 
                                                    'vp-numpy-style-flex-row-center');
                    sbTagString.appendLine("<div style='margin:0 5px;'>");
                    sbTagString.appendFormatLine("<span class='{0}' data-caption-id='{1}'>", 'vp-multilang', 'length-kor');
                    sbTagString.appendFormatLine("{0}", 'Length :');
                    sbTagString.appendLine("</span>");
                    sbTagString.appendFormatLine("<input type='text' class='{0} {1} {2}' value='{3}'/>", 
                                                        'vp-numpy-input', 'vp-numpy-oneArrayEditor-length-input', 
                                                        `vp-numpy-oneArrayEditor-length-input-${uuid}`, this.getOneArrayLength());
                    sbTagString.appendLine("</div>");
                    sbTagString.appendFormatLine("<button class='{0} {1}' data-caption-id='{2}'>", 
                                                          'vp-numpy-func_btn', `vp-numpy-oneArrayEditor-make-btn-${uuid}` ,'new');
                    sbTagString.appendFormatLine("{0}", 'New');
                    sbTagString.appendLine("</button>");
                    sbTagString.appendLine("</div>");
                    dom = $(sbTagString.toString()); 
                    baseDom.append(dom);
                }
              
        

                /**  1차원 배열 길이를 입력하는 이벤트 함수  */
                $(importPackageThis.wrapSelector(`.vp-numpy-oneArrayEditor-length-input-${uuid}`)).on(STR_CHANGE_KEYUP_PASTE, function() {
                    that.setOneArrayLength ( parseInt($(this).val()) );
                });

                /**  입력한 길이 숫자 만큼의 1차원 배열을 생성하는 이벤트 함수  */
                $(importPackageThis.wrapSelector(`.vp-numpy-oneArrayEditor-make-btn-${uuid}`)).click(function() {
                    var newArray = [];
                    for(var i = 0; i <  that.getOneArrayLength(); i++){
                        newArray.push('0');
                    }
                    numpyState.setState({
                        paramData: {
                            [`${stateParamName}`]: newArray
                        }
                    });
                    that.renderParamOneArrayEditor(tagSelector, stateParamName);
                });
                break;
            }
            case 'JY902':{
                /** 2차원 배열 행의 길이를 구하는 로직 */
                this.setTwoArrayRow(numpyState.getState(stateParamName).length);

                /** 2차원 배열 열의 길이를 구하는 로직 */
                var maxColNum = 0;
                this.getState(stateParamName).forEach(elementArray => {
                    var num = elementArray.length;
                    maxColNum = Math.max(maxColNum, num);
                });
                this.setTwoArrayCol(maxColNum);

                /** 2차원 행 열 값 입력 <div>블럭 생성 */
                {
                    var sbTagString = new sb.StringBuilder();
   
                    sbTagString.appendFormatLine("<div class='{0}' style='margin-bottom:5px;'>", 
                                                       'vp-numpy-style-flex-row-center');
                    sbTagString.appendLine("<div style='margin:0 5px;'>");
                    sbTagString.appendFormatLine("<span  class='{0}' data-caption-id='{1}'>", 'vp-multilang', 'row-kor');
                    sbTagString.appendFormatLine("{0}", 'Row :');
                    sbTagString.appendLine("</span>");
                    sbTagString.appendFormatLine("<input type='text' class='{0} {1} {2}' value='{3}'/>", 
                                                        'vp-numpy-input', 'vp-numpy-twoArrayEditor-row-input', 
                                                        `vp-numpy-twoArrayEditor-row-input-${uuid}`, this.getTwoArrayRow());
                    sbTagString.appendLine("</div>");

                    sbTagString.appendLine("<div style='margin:0 5px;'>");
                    sbTagString.appendFormatLine("<span  class='{0}' data-caption-id='{1}'>", 'vp-multilang', 'col-kor');
                    sbTagString.appendFormatLine("{0}", 'Col :');
                    sbTagString.appendLine("</span>");
                    sbTagString.appendFormatLine("<input type='text' class='{0} {1} {2}' value='{3}'/>", 
                                                    'vp-numpy-input', 'vp-numpy-twoArrayEditor-col-input', 
                                                    `vp-numpy-twoArrayEditor-col-input-${uuid}`, this.getTwoArrayCol());
                    sbTagString.appendLine("</div>");

                    sbTagString.appendFormatLine("<button  class='{0} {1}' data-caption-id='{2}' />", 
                                                    'vp-numpy-func_btn', `vp-numpy-twoArrayEditor-make-btn-${uuid}`, 'New');

                    sbTagString.appendLine("</div>");
                    dom = $(sbTagString.toString()); 
                    baseDom.append(dom);
                }

                /** 2차원 배열 행의 길이 값을 입력하는 이벤트 함수 */
                $(importPackageThis.wrapSelector(`.vp-numpy-twoArrayEditor-row-input-${uuid}`)).on('change keyup paste', function() {
                    numpyPageRenderThis.setTwoArrayRow( parseInt( $(this).val() ) );
                });
                /** 2차원 배열 열의 길이 값을 입력하는 이벤트 함수 */
                $(importPackageThis.wrapSelector(`.vp-numpy-twoArrayEditor-col-input-${uuid}`)).on('change keyup paste', function() {
                    numpyPageRenderThis.setTwoArrayCol( parseInt( $(this).val() ) );
                });

                /** 입력한 행과 열의 숫자 만큼의 2차원 배열 을 생성하는 이벤트 함수 */
                $(importPackageThis.wrapSelector(`.vp-numpy-twoArrayEditor-make-btn-${uuid}`)).click(function() {
                    var newTwoArray = [];
                    for(var i = 0; i < numpyPageRenderThis.getTwoArrayRow(); i++){
                        newTwoArray.push([]);
                        for(var j = 0; j < numpyPageRenderThis.getTwoArrayCol(); j++){
                            newTwoArray[i].push('0');
                        }
                    }
                    numpyStateGenerator.setState({
                        paramData: {
                            [`${stateParamName}`]: newTwoArray
                        }
                    });

                    /** 2차원 배열 생성 버튼을 클릭하면 입력한 행과 열의 숫자 만큼의 2차원 배열을 다시 렌더링 */
                    numpyPageRenderThis.renderParamTwoArrayEditor(tagSelector, stateParamName);
                });

                break;
            }
            case 'JY903':{

            }
        }
    }

    NumpyRenderer.prototype.renderParamOneArrayEditor = function(tagSelector, stateParamName) {
        var that = this;
        var importPackageThis = this.getImportPackageThis();
        var numpyState = this.getNumpyState();

        var onearrayDom = $(importPackageThis.wrapSelector(tagSelector));

        this.resetArrayEditor(onearrayDom);
        this.renderParamArrayEditorTitle(onearrayDom, tagSelector, stateParamName, 'JY901');

        var flexRowDiv = renderDiv({'class':'vp-numpy-style-flex-row-wrap'});
        /**, 
         * numpyState.getState(stateParamName) 배열의 인덱스 갯수만큼 for문 돌아 편집기 생성
         */
        var oneArrayState = numpyState.getState(stateParamName);
        for (var i = 0; i < oneArrayState.length; i++) {

            (function(j) {
                var oneArrayStateElement = numpyState.getState(stateParamName)[j];
                var oneArrayBlockDiv = renderDiv({'class':'vp-numpy-style-flex-column' 
                                                    ,'style':'margin-top:10px; margin-bottom:10px;'});
                var oneArrayBlockIndexDiv = renderDiv({'class':'text-center' 
                                                        ,'style':'margin-top:10px; margin-bottom:10px;'
                                                        ,'text': `${j}`});
                var oneArrayBlockInput = renderInput({'class':'vp-numpy-input text-center' 
                                                     , 'style':'width:40px;'
                                                     , 'text': `${j}`
                                                     , 'type': 'text'
                                                     , 'value': `${oneArrayStateElement}`});
                var deleteButton = renderButton({ 'class':'vp-numpy-func_btn'
                                                         , 'style': 'width:40px;'
                                                         , 'text':'x'});
                oneArrayBlockDiv.append(oneArrayBlockIndexDiv);
                oneArrayBlockDiv.append(oneArrayBlockInput);
                oneArrayBlockDiv.append(deleteButton);
                flexRowDiv.append(oneArrayBlockDiv);
                onearrayDom.append(flexRowDiv);

                /**
                 *  1차원 배열 값 변경
                 */
                $(oneArrayBlockInput).on(STR_CHANGE_KEYUP_PASTE, function() {
                    var updatedIndexValue = $(this).val();
                    var updatedParamOneArray = updateOneArrayValueAndGet(numpyState.getState(stateParamName), j, updatedIndexValue);
                    numpyState.setState({
                        [`${stateParamName}`]: updatedParamOneArray
                    });
                });
              
                /**
                 *  1차원 배열 값 삭제
                 */
                $(deleteButton).click(function() {
                    var deletedParamOneArray = deleteOneArrayValueAndGet(numpyState.getState(stateParamName),j);
                    numpyState.setState({
                        [`${stateParamName}`]: deletedParamOneArray
                    });
                    that.renderParamOneArrayEditor(tagSelector, stateParamName);
                });
            })(i);
        }

        onearrayDom.parent().find(`.vp-numpy-array-oneArray-func-plusbtn-${stateParamName}`).off();
        onearrayDom.parent().find(`.vp-numpy-array-oneArray-func-plusbtn-${stateParamName}`).remove();
        
        var plusButton = renderButton({ 'class': `vp-numpy-func_btn 
                                                  vp-numpy-array-oneArray-func-plusbtn-${stateParamName}`
                                        , 'style': 'width: 100%; padding: 1rem;' });
        var span = renderSpan({'class':'vp-multilang'
                                , 'data_caption_id':'numpyPlus'
                                , 'text': '+ Plus'});
        plusButton.append(span);
        onearrayDom.parent().append(plusButton);
    
        /**   - 1차원 배열 생성 클릭 - */
        $(plusButton).click( function() {
            numpyState.setState({
                [`${stateParamName}`]: [...numpyState.getState(stateParamName), '0']
            });
            numpyPageRenderThis.renderParamOneArrayEditor(tagSelector, stateParamName);
            /**  
             * - 1차원 배열 생성 버튼 클릭 후 배열 다시 렌더링
            */
        });

    }
    return NumpyRenderer;
});

  