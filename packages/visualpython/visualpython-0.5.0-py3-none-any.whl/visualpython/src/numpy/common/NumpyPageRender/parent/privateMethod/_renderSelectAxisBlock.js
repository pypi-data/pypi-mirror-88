define ([     
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/StringBuilder'
], function( vpCommon, sb ) {
    /**
     * _renderSelectAxisBlock
     * numpy 옵션 Axis를 편집하는 html태그를 동적 렌더링
     * @param {numpyPageRenderer this} numpyPageRendererThis 
     */
    var _renderSelectAxisBlock = function(numpyPageRendererThis) {
        var uuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();
        var numpyAxisArray = numpyPageRendererThis.numpyAxisArray;
        
        var optionPageSelector = numpyPageRendererThis.getOptionPageSelector();
        var optionPage = $(numpyPageRendererThis.importPackageThis.wrapSelector(optionPageSelector));

        /**
         *  indexNBlock
         *  Axis 편집 동적 태그 블럭
         */
        // var indexNBlock = $(`<div class='vp-numpy-option-block vp-spread' id='vp_blockArea'
        //                           style='padding-top: 10px;'>
        //                         <table style='width: 100%;'>
        //                             <tr>
        //                                 <td style='width: 40%;'>
        //                                     <label class='vp-multilang' data-caption-id='Select Axis'
        //                                            style='margin-bottom: 0px;'> 
        //                                         Select Axis
        //                                     </label>
        //                                 </td>
                                        
        //                                 <td>
        //                                     <select class='vp-numpy-select-indexN' id='vp_numpyIndexN-${uuid}'>
        //                                     </select>
        //                                 </td>
        //                             </tr>
        //                         </table>

        //                     </div>`);
        var sbTagString = new sb.StringBuilder();
        sbTagString.appendLine( `<tr class='vp-numpy-option-block'>`);
        sbTagString.appendLine(`<th>Select Axis</th>`)
        sbTagString.appendLine( `<td>`);
        sbTagString.appendFormatLine("<select class='vp-numpy-select-indexN' id='{0}'>", `vp_numpyIndexN-${uuid}` );
        sbTagString.appendLine("</select>" );

        sbTagString.appendLine( `</td>`);
        sbTagString.appendLine( `<tr>`);
        optionPage.append(sbTagString.toString());

        /**
         * numpyAxis 배열을 option 태그에 동적 렌더링 
         */ 
        numpyAxisArray.forEach((element) => {
            $(importPackageThis.wrapSelector(`#vp_numpyIndexN-${uuid}`)).append(`<option value='${element}'> ${element}</option>`)
        });

        /**
         * Axis change 이벤트 함수
         */
        $(importPackageThis.wrapSelector(`#vp_numpyIndexN-${uuid}`)).change(function() {
            numpyStateGenerator.setState({
                axis: $(':selected', this).val()
            });
        });
    }
    return _renderSelectAxisBlock;
});
