define ([    
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/StringBuilder'
], function( vpCommon, sb ) {
    /** 
     * return 변수를 편집하는 html태그를 동적 렌더링
     * @param {numpyPageRenderer this} numpyPageRendererThis 
     */
    var _renderReturnVarBlock = function(numpyPageRendererThis) {
        var uuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;

        /**
         * return 변수 동적 태그 블럭
         */
        var sbTagString = new sb.StringBuilder();
        // sbTagString.appendFormatLine("<div class='{0} {1}' id='{2}' style='padding-top: 10px;'>", 
        //                                 'vp-numpy-option-block', 'vp-spread', 'vp_blockArea');
        // sbTagString.appendLine("<table style='width: 100%;'>" );
        // sbTagString.appendLine("<tr>" );
        // sbTagString.appendLine("<td style='width: 40%;'>" );
        // sbTagString.appendFormatLine("<label class='{0}' data-caption-id='{1}' style='margin-bottom: 0px;'> ",
        //                                      'vp-multilang', 'inputReturnVariable');
        // sbTagString.appendFormatLine("{0}", 'Input Return Variable');
        // sbTagString.appendLine("</label>" );
        // sbTagString.appendLine("</td>" );
        // sbTagString.appendLine("<td>" );
        // sbTagString.appendFormatLine("<input type='text' class='{0} {1}' id='{2}' placeholder='{3}'/>", 
        //                                     'vp-numpy-input', 'vp-numpy-return-input', `vp_numpyReturnVarInput-${uuid}`, 'input variable');
        // sbTagString.appendLine("</td>" );
        // sbTagString.appendLine("</tr>" );
        // sbTagString.appendLine("</table>" );
        // sbTagString.appendLine("</div>" );
        var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();
        var returnVariableState = numpyStateGenerator.getState('returnVariable');
        sbTagString.appendLine( `<tr class='vp-numpy-option-block'>`);
        sbTagString.appendLine(`<th>Input Return Variable</th>`)
        sbTagString.appendLine( `<td>`);
      
        sbTagString.appendFormatLine("<input type='text' class='{0} {1}' id='{2}' placeholder='{3}' value='{4}'/>", 
                                            'vp-numpy-input', 'vp-numpy-return-input', `vp_numpyReturnVarInput-${uuid}`, 'input variable'
                                            , returnVariableState);

        sbTagString.appendLine( `</td>`);
        sbTagString.appendLine( `<tr>`);

        var returnVarBlock = $(sbTagString.toString()); 
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();
       
        var optionPageSelector = numpyPageRendererThis.getOptionPageSelector();
        var optionPage = $(importPackageThis.wrapSelector(optionPageSelector));
        optionPage.append(returnVarBlock);

        /** return 변수 입력 */
        $(importPackageThis.wrapSelector(`#vp_numpyReturnVarInput-${uuid}`)).on('change keyup paste', function() {
            numpyStateGenerator.setState({
                returnVariable: $(this).val()
            });
        });

        // return 변수 print 여부 선택
        $(importPackageThis.wrapSelector(`#vp_numpyInputCheckBox-${uuid}`)).click(function() {
            numpyStateGenerator.setState({
                isReturnVariable: $(this).is(':checked')
            });
        });                
    }

    return _renderReturnVarBlock;
});
