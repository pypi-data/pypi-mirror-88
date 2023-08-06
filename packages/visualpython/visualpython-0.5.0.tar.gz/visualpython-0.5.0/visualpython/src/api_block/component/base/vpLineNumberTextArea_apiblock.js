/** src/common에 있는 vpLineNumberTextArea을 api block에 맞게 커스텀 */define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/component/vpLineNumberTextArea'

    , '../../api.js'    
    , '../../config.js'
    , '../../constData.js'
    , '../../blockRenderer.js'
    
], function ( $, vpCommon, vpConst, sb, vpLineNumberTextArea,
              api, config, constData, blockRenderer ) {
                  
    var vpLineNumberTextArea_apiblock = function(id, codeState) {
        var lineNumberTextArea = new vpLineNumberTextArea.vpLineNumberTextArea( id, 
                                                                                codeState);                                                                 
        var lineNumberTextAreaStr = lineNumberTextArea.toTagString();
        return lineNumberTextAreaStr;
    }
    return vpLineNumberTextArea_apiblock;
});