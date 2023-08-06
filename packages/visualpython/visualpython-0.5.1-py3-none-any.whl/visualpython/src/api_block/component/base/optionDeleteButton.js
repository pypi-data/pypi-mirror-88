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

    const { VP_CLASS_STYLE_FLEX_COLUMN_CENTER } = constData;

    var MakeOptionDeleteButton = function(id) {
        var sbOptionDeleteButton = new sb.StringBuilder();
        sbOptionDeleteButton.appendFormatLine("<div id='{0}' class='{1}'>", id, VP_CLASS_STYLE_FLEX_COLUMN_CENTER);
        sbOptionDeleteButton.appendFormatLine("<div class='{0} {1}'>",'vp-apiblock-icon-btn' ,'vp-apiblock-del-col');
        sbOptionDeleteButton.appendLine("</div>");
        sbOptionDeleteButton.appendLine("</div>");

        sbOptionDeleteButton =  sbOptionDeleteButton.toString();
        return sbOptionDeleteButton;
    }
    return MakeOptionDeleteButton;
});
