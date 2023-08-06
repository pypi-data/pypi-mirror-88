define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'

    , '../../api.js'    
    , '../../config.js'
    , '../../constData.js'
    , '../../blockRenderer.js'
    
], function ( $, vpCommon, vpConst, sb, 
              api, config, constData, blockRenderer ) {
    const             {VP_CLASS_STYLE_FLEX_ROW_CENTER} = constData;
    var MakeOptionInput = function(id, className, value, placeholder) {
        var sbOptionInput = new sb.StringBuilder();
        sbOptionInput.appendFormatLine("<input type='text' class='{0} {1}'", VP_CLASS_STYLE_FLEX_ROW_CENTER, className);
        sbOptionInput.appendFormatLine("     id='{0}' ", id);
        sbOptionInput.appendFormatLine("     value='{0}' ", value);
        sbOptionInput.appendFormatLine("     placeholder='{0}' ", placeholder);
        sbOptionInput.appendFormatLine("     style='{0}' >", '');
        sbOptionInput.appendLine("</input>");
        sbOptionInput = sbOptionInput.toString();
        return sbOptionInput;
    }
    return MakeOptionInput;
});