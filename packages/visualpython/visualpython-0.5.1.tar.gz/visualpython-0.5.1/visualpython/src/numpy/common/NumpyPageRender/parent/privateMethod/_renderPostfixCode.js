define ([    
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/component/vpLineNumberTextArea'
], function( vpCommon, sb, vpLineNumberTextArea ) {

    var _renderPostfixCode = function(numpyPageRendererThis) {
        var uuid = vpCommon.getUUID();
        var newUuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();
        var rootTagSelector = numpyPageRendererThis.getRootTagSelector();
 
        var postfixCodeState = numpyStateGenerator.getState('postfixCode');
 
        var lineNumberTextArea = new vpLineNumberTextArea.vpLineNumberTextArea( `vp-numpy-postfix-textarea`+ uuid, 
                                                                                 postfixCodeState);                                                                 
        var lineNumberTextAreaStr = lineNumberTextArea.toTagString();

        var postfixDom = $(`<div class="${uuid} vp-accordion-container    vp-accordion-gray-color">
                                <div class="vp-accordion-header">
                                    <span class="vp-accordion-indicator"></span>
                                    <span class="vp-accordion-caption">Postfix Code</span>
                                    </div>
                                    <div class="vp-accordion-content"><div class="${newUuid}">
                                        ${lineNumberTextAreaStr}
                                    </div>
                                </div>
                            </div>`);
        var mainPage = $(importPackageThis.wrapSelector(rootTagSelector));
        mainPage.append(postfixDom);

        mainPage.on('focus', '.vp-numpy-postfix-textarea', function() {
            Jupyter.notebook.keyboard_manager.disable();
        });
        mainPage.on('blur', '.vp-numpy-postfix-textarea', function() {
            Jupyter.notebook.keyboard_manager.enable();
        });

        /** postfix Code */
        $(document).off('change keyup paste', '#' + 'vp-numpy-postfix-textarea'+ uuid);
        $(document).on('change keyup paste', '#' + 'vp-numpy-postfix-textarea'+ uuid, function(event) {
            numpyStateGenerator.setState({
                postfixCode: $(this).val()
            });
            event.stopPropagation();
        });

    }
    return _renderPostfixCode;
});
