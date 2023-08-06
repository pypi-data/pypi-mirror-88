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

    const { STR_SELECTED } = constData;
    var MakeSelectBox = function(id, className, stateValue, optionDataList) {
        var sbSelectBox = new sb.StringBuilder();
        sbSelectBox.appendFormatLine("<select id='{0}' class='{1}' style='{2}'> ", id , className, '');
        optionDataList.forEach(optionData => {
            // if (optionData == 'default') {
            //     sbSelectBox.appendFormatLine("<option {0} value='{1}'>{2}</option>", STR_SELECTED, '', optionData);
            // } else 
            if (stateValue == optionData) {
                sbSelectBox.appendFormatLine("<option {0} value='{1}'>{2}</option>", STR_SELECTED, optionData, optionData);
            } else {
                sbSelectBox.appendFormatLine("<option value='{0}'>{1}</option>", optionData, optionData);
            }
        });
        sbSelectBox.appendLine("</select>");
        sbSelectBox =  sbSelectBox.toString();
        return sbSelectBox;
    }
    return MakeSelectBox;
});