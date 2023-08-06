define ([    
    'nbextensions/visualpython/src/common/vpCommon'
    ,'nbextensions/visualpython/src/numpy/api/numpyStateApi' 
    , 'nbextensions/visualpython/src/common/StringBuilder'
], function( vpCommon, numpyStateApi, sb ) {
    var { deleteOneArrayIndexValueAndGetNewArray } = numpyStateApi;

    var _renderUserOption = function(numpyPageRendererThis) {
        var uuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();

        var rootTagSelector = numpyPageRendererThis.getRootTagSelector();
        var mainPage = $(importPackageThis.wrapSelector(rootTagSelector));

        var sbTagString = new sb.StringBuilder();
        sbTagString.appendFormatLine("<div class='{0} {1} {2}' >", 'vp-numpy-block', 'vp-numpy-useroption', 'vp-minimize' );
        sbTagString.appendFormatLine("<div class='{0}'>", 'vp-accordion-header');
        sbTagString.appendFormatLine("<div class='{0} {1} ' ></div>", 'vp-panel-area-vertical-btn', 'vp-arrow-down' );
        sbTagString.appendFormatLine("<span class='{0}' data-caption-id='{1}'>", 'vp-multilang', 'Variable');
        sbTagString.appendFormatLine("{0}", 'User Option');
        sbTagString.appendLine("</span>");
        sbTagString.appendLine("</div>");
        sbTagString.appendFormatLine("<div id='{0}' class='{1}' >", 'vp_userOption', 'vp-list-container');
        sbTagString.appendFormatLine("<table class='{0} {1}' style='width:100%;'>", 
                                            'vp-tbl-search-result', 'vp-numpy-useroption-table');
        sbTagString.appendLine("</table>");
        sbTagString.appendLine("</div>");
        sbTagString.appendLine("</div>");
        var userOptionDom = $(sbTagString.toString()); 
    
        mainPage.append(userOptionDom);    
        var userOptionTable = $('.vp-numpy-useroption-table');

        var renderUserOptionList = () => {
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
            for (var i = 0; i < numpyStateGenerator.getState('userOptionList').length; i++) {
                (function(j) {

                    var optionKey = numpyStateGenerator.getState('userOptionList')[j].optionKey;
                    var optionValue = numpyStateGenerator.getState('userOptionList')[j].optionValue;
    
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
                    $(importPackageThis.wrapSelector(`.vp-numpy-useroption-key-${j}-${uuid}`)).on('change keyup paste', function() {
                        var updatedIndexValue = $(importPackageThis.wrapSelector(`.vp-numpy-useroption-key-${j}-${uuid}`)).val();
                        numpyStateGenerator.getState('userOptionList')[j].optionKey = updatedIndexValue;
                    });
    
                    $(importPackageThis.wrapSelector(`.vp-numpy-useroption-value-${j}-${uuid}`)).on('change keyup paste', function() {
                        var updatedIndexValue = $(importPackageThis.wrapSelector(`.vp-numpy-useroption-value-${j}-${uuid}`)).val();
                        numpyStateGenerator.getState('userOptionList')[j].optionValue = updatedIndexValue;
                    });
    
                    /**
                     *  값 삭제
                     */
                    $(importPackageThis.wrapSelector(`.vp-numpy-useroption-deleteBtn-${j}-${uuid}`)).click(function() {
                        var deletedParamOneArray = deleteOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState('userOptionList'),j);
        
                        numpyStateGenerator.setState({
                            userOptionList: deletedParamOneArray
                        });
        
                        renderUserOptionList();
                    });
                })(i);;
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
                numpyStateGenerator.setState({
                    userOptionList: [...numpyStateGenerator.getState('userOptionList'), newData]
                });

                renderUserOptionList();    
            });
        }
        renderUserOptionList();
    }

    return _renderUserOption;
});
