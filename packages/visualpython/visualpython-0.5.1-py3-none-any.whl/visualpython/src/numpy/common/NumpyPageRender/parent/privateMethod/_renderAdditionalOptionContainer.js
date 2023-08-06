define ([    
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/StringBuilder'
], function( vpCommon, sb ) {

    var _renderAdditionalOptionContainer = function(numpyPageRendererThis) {
        var uuid = vpCommon.getUUID();
        var newUuid = vpCommon.getUUID();

        var numpyPageRendererThis = numpyPageRendererThis;
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
     
        var rootTagSelector = numpyPageRendererThis.getRootTagSelector();
        var optionPage = $(importPackageThis.wrapSelector(rootTagSelector));

        // var sbTagString = new sb.StringBuilder();
        // sbTagString.appendFormatLine("<div class='{0} {1} {2}' >", 'vp-numpy-optionPageBlock-view', 'vp-numpy-block', 'vp-minimize' );
        // sbTagString.appendFormatLine("<div class='{0}'>", 'vp-accordion-header');
        // sbTagString.appendFormatLine("<div class='{0} {1}' >", 'vp-panel-area-vertical-btn', 'vp-arrow-down');
        // sbTagString.appendLine("</div>");
        // sbTagString.appendFormatLine("<span class='{0}' data-caption-id='{1}'>", 'vp-multilang', 'Variable');
        // sbTagString.appendFormatLine("{0}", 'Additional Options');
        // sbTagString.appendLine("</span>");
        // sbTagString.appendLine("</div>");
        // sbTagString.appendLine("</div>");

        // $(`<div class="vp-numpy-optionPageBlock-view vp-numpy-block vp-spread">
        //         <div class="vp-accordion-header">
        //         <div class="vp-panel-area-vertical-btn vp-arrow-right">
        //     </div>
        //     <span class="vp-multilang" data-caption-id="Variable">
        //          Additional Options
        //     </span>
        //         </div>
        //         <div class="vp-numpy-option-block vp-spread" id="vp_blockArea" style="padding-top: 10px;">
        //         <table style="width: 100%;">
        //         <tbody><tr>
        //         <td style="width: 40%;">
        //         <label class="vp-multilang" data-caption-id="inputReturnVariable" style="margin-bottom: 0px;"> 
        //         Input Return Variable
        //         </label>
        //         </td>
        //         <td>
        //         <input type="text" class="vp-numpy-input vp-numpy-return-input" id="vp_numpyReturnVarInput-43bcbb88-c84a-418b-b170-f85867deaaab" placeholder="input variable">
        //         </td>
        //         </tr>
        //         </tbody></table>
        //     </div></div>`);

        var additionalOptionDom =    $(`<div class="${uuid} vp-accordion-container">
                    <div class="vp-accordion-header">
                    <span class="vp-accordion-indicator"></span>
                    <span class="vp-accordion-caption">Additional Option</span>
                    </div>
                    <div class="vp-accordion-content"><table class="${newUuid} 
                            vp-option-vertical-table-layout ">
                    <colgroup><col width="30%"><col width="*"></colgroup>
                    <tbody class="vp-numpy-optionPageBlock-view vp-numpy-block">

                        </tbody>
                    </table>
                    </div>
                </div>`)
        // var additionalOptionDom = $(sbTagString.toString());  
        optionPage.append(additionalOptionDom);

    }
    return _renderAdditionalOptionContainer;
});
