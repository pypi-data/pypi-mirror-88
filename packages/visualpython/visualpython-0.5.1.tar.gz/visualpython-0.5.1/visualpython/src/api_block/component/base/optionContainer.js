define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'

    , '../../api.js'    
    , '../../config.js'
    , '../../constData.js'
    , '../../blockRenderer.js'


], function ( $, vpCommon, vpConst, sb    

             , api
             , config
             , constData
             , blockRenderer ){

    const { VP_CLASS_STYLE_FLEX_ROW_CENTER
            , VP_CLASS_STYLE_FLEX_COLUMN_CENTER } = constData;

    var MakeOptionContainer = function() {
        var sbOptionContainer = new sb.StringBuilder();
        sbOptionContainer.appendFormatLine("<div class='{0}'  ", VP_CLASS_STYLE_FLEX_ROW_CENTER);
        sbOptionContainer.appendFormatLine("     style='{0}' >", 'padding: 0.5rem;');
        sbOptionContainer.appendFormatLine("<div class='{0} {1}' >", 'vp-apiblock-option', 
                                                                      VP_CLASS_STYLE_FLEX_COLUMN_CENTER);
        sbOptionContainer.appendLine("</div>");
        sbOptionContainer.appendLine("</div>");
        sbOptionContainer = $(sbOptionContainer.toString());

        return sbOptionContainer.find('.vp-apiblock-option');
    }

    return MakeOptionContainer;
});