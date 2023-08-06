define ([    
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/component/vpLineNumberTextArea'
], function( vpCommon, sb, vpLineNumberTextArea ) {

    var _renderPrefixCode = function(numpyPageRendererThis) {
        var uuid = vpCommon.getUUID();
        var newUuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();
        var rootTagSelector = numpyPageRendererThis.getRootTagSelector();

        var prefixCodeState = numpyStateGenerator.getState('prefixCode');
 
        var lineNumberTextArea = new vpLineNumberTextArea.vpLineNumberTextArea( `vp-numpy-prefix-textarea`+ uuid, 
                                                                                prefixCodeState);                                                                 
        var lineNumberTextAreaStr = lineNumberTextArea.toTagString();
        var prefixDom = $(`<div class="${uuid} vp-accordion-container    
                                    vp-accordion-gray-color">
                                <div class="vp-accordion-header">
                                    <span class="vp-accordion-indicator"></span>
                                    <span class="vp-accordion-caption">Prefix Code</span>
                                    </div>
                                    <div class="vp-accordion-content"><div class="${newUuid}">
                                        ${lineNumberTextAreaStr}
                                       
                                    </div>
                                </div>
                            </div>`);

                
        var mainPage = $(importPackageThis.wrapSelector(rootTagSelector));
        mainPage.append(prefixDom);

        mainPage.on('focus', '.vp-numpy-prefix-textarea', function() {
            Jupyter.notebook.keyboard_manager.disable();
        });
        mainPage.on('blur', '.vp-numpy-prefix-textarea', function() {
            Jupyter.notebook.keyboard_manager.enable();
        });    

        /** prefix Code */
        $(document).off('change keyup paste', '#' + 'vp-numpy-prefix-textarea'+ uuid);
        $(document).on('change keyup paste', '#' + 'vp-numpy-prefix-textarea'+ uuid, function(event) {
            numpyStateGenerator.setState({
                prefixCode: $(this).val()
            });
            event.stopPropagation();
        });
        


    }
    return _renderPrefixCode;
});
