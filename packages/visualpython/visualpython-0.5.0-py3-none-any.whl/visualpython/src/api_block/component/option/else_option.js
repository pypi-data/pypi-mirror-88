define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'

    , '../../api.js'    
    , '../../config.js'
    , '../../constData.js'
    , '../../blockRenderer.js'
    , '../base/index.js'
], function ( $, vpCommon, vpConst, sb, 
            //   block
              api
              , config
              , constData
              , blockRenderer
              , baseComponent ) {


    const { MakeOptionContainer } = baseComponent;
    var InitElseBlockOption = function(thatBlock, optionPageSelector) {
        var renderThisComponent = function() {
            var elseBlockOption = MakeOptionContainer();
            elseBlockOption.append('<div>(N/A)</div>');

            /**block option 탭에 렌더링된 dom객체 생성 */
            $(optionPageSelector).append(elseBlockOption);
        }
        renderThisComponent();
    }

    return InitElseBlockOption;
});