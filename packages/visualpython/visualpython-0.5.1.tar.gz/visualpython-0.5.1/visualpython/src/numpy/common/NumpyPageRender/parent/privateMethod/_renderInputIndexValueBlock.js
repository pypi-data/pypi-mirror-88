define ([    
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/StringBuilder'
], function( vpCommon, sb ) {

    /** numpy의 옵션 중 indexValue를 입력하는 블럭을 동적 렌더링하는 메소드
     * numpy의 특정 함수들이 indexValue 옵션을 지정 할 수 도 안할 수도 있다.
     * @param {numpyPageRenderer this} numpyPageRendererThis
     * @param {title} title
     * @param {string || Array<string>} stateParamNameOrArray
    */
    var _renderInputIndexValueBlock = function(numpyPageRendererThis, title, bindFuncData) {
    
        var uuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        var rootTagSelector = numpyPageRendererThis.getRequiredPageSelector();

        var rootPage = $(importPackageThis.wrapSelector(rootTagSelector));
        // var indexValueBlock = $(`<div class='vp-numpy-option-block vp-spread' 
        //                               id='vp_blockArea'
        //                               style='padding-top:10px;'>
        //                             <table style='width: 100%;'>
        //                                 <tr>
        //                                     <td style='width: 40%;'>
        //                                         <span>*</span>
        //                                         <label for='i0' class='vp-multilang' data-caption-id='inputIndex'
        //                                             style='margin-bottom: 0px;'> 
        //                                             ${title}
        //                                         </label>
        //                                     </td>
                                            
        //                                     <td class='vp-numpy-${uuid}-block'>
                                
        //                                     </td>
        //                                 </tr>
        //                             </table>
   
        //                         </div>`);
        var sbTagString = new sb.StringBuilder();
        sbTagString.appendLine( `<tr class='vp-numpy-option-block'>`);
        sbTagString.appendLine(`<th>${title}</th>`)
        sbTagString.appendLine( `<td class='vp-numpy-${uuid}-block'>`);
        // sbTagString.appendFormatLine("<input type='text' class='{0} {1}' id='{2}' placeholder='{3}'/>", 
        //                                'vp-numpy-input', 'vp-numpy-callVar-input', `vp_numpyCallVarInput-${uuid}`, 'input variable');
                                // sbTagString.appendFormatLine("<select class='vp-numpy-select-dtype' id='{0}'>", `vp_numpyDtype-${uuid}` );
                                // sbTagString.appendLine("</select>" );
        sbTagString.appendLine( `</td>`);
        sbTagString.appendLine( `<tr>`);
        rootPage.append(sbTagString.toString());

        // numpyPageRendererThis.renderParamInputArrayEditor(`.vp-numpy-${uuid}-block`, bindFuncData, false)
      numpyPageRendererThis.renderParamInputArrayEditor(`.vp-numpy-${uuid}-block`, bindFuncData, false)
    }

    return _renderInputIndexValueBlock;
});
