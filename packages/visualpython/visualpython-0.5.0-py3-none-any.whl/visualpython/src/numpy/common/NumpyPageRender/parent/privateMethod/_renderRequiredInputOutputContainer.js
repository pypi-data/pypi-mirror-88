define ([    
    'nbextensions/visualpython/src/common/vpCommon'
], function( vpCommon ) {

    var _renderRequiredInputOutputContainer = function(numpyPageRendererThis) {
        var uuid = vpCommon.getUUID();
        var newUuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;
        // var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        // var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();
     
        var rootTagSelector = numpyPageRendererThis.getRootTagSelector();
        var optionPage = $(numpyPageRendererThis.importPackageThis.wrapSelector(rootTagSelector));


        var additionalOptionDomElement = $(`<div class="${uuid} vp-accordion-container vp-accordion-open  ">
                <div class="vp-accordion-header">
                <span class="vp-accordion-indicator"></span>
                <span class="vp-accordion-caption">Required Input</span>
                </div>
                <div class="vp-accordion-content">
                <table class="${newUuid} 
                    vp-option-vertical-table-layout  vp-th-highlight">
                <colgroup><col width="25%"><col width="*"></colgroup>
                <tbody class='vp-numpy-requiredPageBlock-tbody'>
      

                    </tbody>
                </table>
                </div>
                </div>`);
            //     <tr>
            //     <th>Input Parameter</th>
            //     <td>
            //         <div class='vp-numpy-requiredPageBlock-view 
            //                                                 vp-numpy-block '>
            //         </div>
            //     </td>
            // </tr>
        // var additionalOptionDomElement = $(`<div class='vp-numpy-requiredPageBlock-view 
        //                                                 vp-numpy-block '>
        //                                         <div class="vp-accordion-header">
        //                                             <div class='vp-panel-area-vertical-btn vp-arrow-right'></div>
        //                                             <span class='vp-multilang' data-caption-id='TODO:Variable'>
        //                                                 Required Input &amp; Output
        //                                             </span>
        //                                         </div>
        //                                     </div>`);

        optionPage.append(additionalOptionDomElement);

    }
    return _renderRequiredInputOutputContainer;
});
