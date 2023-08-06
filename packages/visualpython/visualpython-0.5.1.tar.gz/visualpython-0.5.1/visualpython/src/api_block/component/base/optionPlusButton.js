define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'

    , 'nbextensions/visualpython/src/common/vpFuncJS'
    , 'nbextensions/visualpython/src/pandas/common/commonPandas'
    , 'nbextensions/visualpython/src/common/vpMakeDom'

    , '../../api.js'    
    , '../../config.js'
    , '../../constData.js'
    , '../../blockRenderer.js'
    
], function ( $, vpCommon, vpConst, sb, 
              vpFuncJS, libPandas, vpMakeDom,
              api, config, constData, blockRenderer ) {

    var MakeOptionPlusButton = function(id, title, className) {
        var sbOptionPlusButton = new sb.StringBuilder();
        sbOptionPlusButton.appendFormatLine("<div id='{0}' class='{1}'> ", id , className);
        sbOptionPlusButton.appendFormatLine("<div class='{0}'> ", 'vp-apiblock-option-plus-button');

        sbOptionPlusButton.appendFormatLine("{0}", title);
        sbOptionPlusButton.appendLine("</div>");
        sbOptionPlusButton.appendLine("</div>");

        // sbOptionPlusButton =  $(sbOptionPlusButton.toString());
        sbOptionPlusButton = sbOptionPlusButton.toString()
        return sbOptionPlusButton;
    }
    return MakeOptionPlusButton;
});
