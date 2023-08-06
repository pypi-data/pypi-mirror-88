define([
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/vpFuncJS'

    , './api.js'
    , './config.js'
    , './constData.js'
    , './shadowBlock.js'
    , './blockRenderer.js'

    , './component/option/class_option.js'
    , './component/option/def_option.js'
    , './component/option/if_option.js'
    , './component/option/elif_option.js'  
    , './component/option/else_option.js'  

    , './component/option/try_option.js'
    , './component/option/except_option.js'  
    , './component/option/for_option.js'
    , './component/option/listfor_option.js'

    , './component/option/import_option.js'  

    , './component/option/code_option.js'

    , './component/option/return_option.js'
    , './component/option/while_option.js'
    , './component/option/lambda_option.js'

    , './component/option/sample_option.js'
    , './component/option/api_option.js'
], function ( vpCommon, vpFuncJS 
    
              , api 
              , config 
              , constData 
              , shadowBlock 
              , blockRenderer

              , InitClassBlockOption
              , InitDefBlockOption
              , InitIfBlockOption
              , InitElifBlockOption
              , InitElseBlockOption

              , InitTryBlockOption
              , InitExceptBlockOption
              , InitForBlockOption
              , InitListForBlockOption

              , InitImportBlockOption

              , InitCodeBlockOption

              , InitReturnBlockOption
              , InitWhileBlockOption
              , InitLambdaBlockOption
              
              , InitSampleBlockOption 
              , InitApiBlockOption) {

    const ShadowBlock = shadowBlock;

    const { ChangeOldToNewState
            , FindStateValue

            , CreateOneArrayValueAndGet
            , UpdateOneArrayValueAndGet
            , DeleteOneArrayValueAndGet

            , DestructureFromBlockArray

            , MakeFirstCharToUpperCase
            , MapTypeToName
            , RemoveSomeBlockAndGetBlockList
            , ShuffleArray
            , GetImageUrl
            
            , MapNewLineStrToSpacebar

            , ControlToggleInput

            , IsCanHaveIndentBlock  
            , IsClassOrDefOrControlBlockType
            , IsCodeBlockType } = api;

    const { PROCESS_MODE } = config;

    const { RenderBlockMainDom
            , RenderBlockLeftHolderDom
            , RenderBlockMainInnerDom
            , RenderBlockMainHeaderDom

            , RenderOptionTitle


            , RenderRunBlockButton
            , RenderDeleteBlockButton


            , RenderHTMLDomColor

            , GenerateClassInParamList
            , GenerateDefInParamList
            , GenerateReturnOutParamList
            , GenerateIfConditionList
            , GenerateForParam
            , GenerateListforConditionList
            , GenerateLambdaParamList
            , GenerateExceptConditionList
            , GenerateImportList
            , GenerateWhileConditionList } = blockRenderer;

    const { BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , BLOCK_DIRECTION
            , BLOCK_TYPE
            , MAKE_CHILD_BLOCK
            , IMPORT_BLOCK_TYPE
            , FOCUSED_PAGE_TYPE

            , DEF_BLOCK_ARG4_TYPE
            , DEF_BLOCK_ARG6_TYPE

            , FOR_BLOCK_TYPE
            , FOR_BLOCK_ARG3_TYPE
            
            , IF_BLOCK_SELECT_VALUE_ARG_TYPE
            , IF_BLOCK_CONDITION_TYPE

            , NUM_BLOCK_HEIGHT_PX
            , NUM_INDENT_DEPTH_PX
            , NUM_MAX_ITERATION
            , NUM_ZERO
            , NUM_HUNDREAD
            , NUM_THOUSAND
            , NUM_DEFAULT_POS_X
            , NUM_DEFAULT_POS_Y
            , NUM_DEFAULT_BLOCK_LEFT_HOLDER_HEIGHT
            , NUM_BLOCK_MARGIN_TOP_PX
            , NUM_BLOCK_MARGIN_BOTTOM_PX
            , NUM_CODELINE_LEFT_MARGIN_PX
            , NUM_EXCEED_DEPTH
            , NUM_FONT_WEIGHT_300
            , NUM_FONT_WEIGHT_700
            , NUM_BLOCK_MAX_WIDTH
            , NUM_BLOCK_BOTTOM_HOLDER_HEIGHT
            , NUM_OPTION_PAGE_WIDTH

            , STR_NULL
            , STR_ONE_INDENT
            , STR_TOP
            , STR_LEFT
            , STR_DIV
            , STR_BORDER
            , STR_PX
            , STR_OPACITY
            , STR_MARGIN_TOP
            , STR_MARGIN_LEFT
            , STR_BOX_SHADOW
            , STR_DISPLAY
            , STR_BACKGROUND_COLOR
            , STR_WIDTH
            , STR_HEIGHT
            , STR_INHERIT
            , STR_YES
            , STR_DATA_NUM_ID 
            , STR_DATA_DEPTH_ID
            , STR_NONE
            , STR_BLOCK
            , STR_SELECTED
            , STR_COLON_SELECTED
            , STR_POSITION
            , STR_STATIC
            , STR_RELATIVE
            , STR_ABSOLUTE
            , STR_COLOR
            , STR_DOT
            , STR_INPUT
            , STR_SPAN
            , STR_CLICK

            , STR_TITLE
            , STR_FONT_WEIGHT
            , STR_SCROLLHEIGHT
            , STR_OVERFLOW_X
            , STR_OVERFLOW_Y
            , STR_HIDDEN
            , STR_AUTO
            , STR_OPTION
            , STR_CLASS
            , STR_DEF
            , STR_IF
            , STR_FOR
            , STR_WHILE
            , STR_IMPORT
            , STR_API
            , STR_TRY
            , STR_EXCEPT
            , STR_RETURN
            , STR_BREAK
            , STR_CONTINUE
            , STR_PASS
            , STR_CODE
            , STR_ELIF
            , STR_PROPERTY
            , STR_SCROLL 
            , STR_ONE_SPACE
            , STR_KEYWORD_NEW_LINE
            , STR_FOCUS 
            , STR_BLUR
            , STR_RIGHT
            , STR_MSG_BLOCK_DELETED
            , STR_MSG_BLOCK_DEPTH_MUSH_NOT_EXCEED_6
            , STR_MSG_AUTO_GENERATED_BY_VISUALPYTHON
            
            , STR_INPUT_YOUR_CODE

            , VP_BLOCK
            , VP_BLOCK_BLOCKCODELINETYPE_CLASS_DEF
            , VP_BLOCK_BLOCKCODELINETYPE_CONTROL
            
            , VP_CLASS_PREFIX

            , VP_CLASS_BLOCK_CONTAINER
            , VP_CLASS_MAIN_CONTAINER
            , VP_CLASS_BLOCK_SHADOWBLOCK
            , VP_CLASS_BLOCK_OPTION_BTN
            , VP_CLASS_BLOCK_DELETE_BTN
            , VP_CLASS_BLOCK_DEPTH_INFO
            , VP_CLASS_BLOCK_NUM_INFO
            , VP_CLASS_BLOCK_CTRLCLICK_INFO
            , VP_CLASS_APIBLOCK_BOARD
            , VP_CLASS_APIBLOCK_OPTION_TAB 
            , VP_CLASS_APIBLOCK_MENU_BTN 
            , VP_CLASS_APIBLOCK_BOTTOM_TAB_VIEW
            , VP_CLASS_APIBLOCK_BOTTOM_OPTIONAL_TAB_VIEW
            , VP_CLASS_BLOCK_LEFT_HOLDER
            , VP_CLASS_BLOCK_BOTTOM_HOLDER
            , VP_CLASS_BLOCK_STYLE_BORDER_TOP_LEFT_RADIUS
            , VP_CLASS_BLOCK_STYLE_BORDER_BOTTOM_LEFT_RADIUS
            , VP_CLASS_BLOCK_SHADOWBLOCK_CONTAINER
            , VP_CLASS_APIBLOCK_MINIMIZE
            , VP_CLASS_APIBLOCK_ARROW_UP
            , VP_CLASS_APIBLOCK_ARROW_DOWN
            , VP_CLASS_APIBLOCK_TAB_NAVIGATION_NODE_OPTION_TITLE_SAPN
            , VP_CLASS_APIBLOCK_TAB_NAVIGATION_NODE_OPTION_CHILDS_TOP_TITLE_SAPN
            , VP_CLASS_APIBLOCK_OPTION_TAB_CHILDS_OPTION
            , VP_CLASS_APIBLOCK_SCROLLBAR

            , VP_CLASS_SELECTED_SHADOWBLOCK
            , VP_CLASS_APIBLOCK_BODY 

            , VP_CLASS_STYLE_FLEX_ROW_BETWEEN
            , VP_CLASS_STYLE_FLEX_ROW_END

            , STR_CHANGE_KEYUP_PASTE

            , STR_ICON_ARROW_UP
            , STR_ICON_ARROW_DOWN
            
            , STR_PHRASE_2PX_SOLID_TRANSPARENT
            , STR_PHRASE_2PX_SOLID_YELLOW
            
            , STATE_classInParamList
            , STATE_className
            , STATE_defName
            , STATE_defInParamList
            
            , STATE_ifCodeLine
            , STATE_isIfElse
            , STATE_isForElse
            , STATE_ifConditionList
            , STATE_elifConditionList

            , STATE_elifCodeLine
            , STATE_elifList
            
            , STATE_forCodeLine
            , STATE_forParam
            , STATE_forBlockOptionType

            , STATE_whileCodeLine
            
            , STATE_baseImportList
            , STATE_isBaseImportPage
            , STATE_customImportList
            
            , STATE_exceptList
            , STATE_exceptCodeLine
            , STATE_isFinally
            , STATE_returnOutParamList
            , STATE_customCodeLine

            , STATE_breakCodeLine
            , STATE_continueCodeLine
            , STATE_passCodeLine
            , STATE_propertyCodeLine
            , STATE_commentLine
            , COLOR_CLASS_DEF
            , COLOR_CONTROL
            , COLOR_CODE
            , COLOR_WHITE
            , COLOR_GRAY_input_your_code
            , COLOR_YELLOW
            , COLOR_BLACK 
            , COLOR_FOCUSED_PAGE

            , COLOR_CLASS_DEF_STRONG
            , COLOR_CONTROL_STRONG
            , COLOR_CODE_STRONG

            , PNG_VP_APIBLOCK_OPTION_ICON
            , PNG_VP_APIBLOCK_DELETE_ICON
        
            , API_BLOCK_PROCESS_DEVELOPMENT
        
            , ERROR_AB0002_INFINITE_LOOP } = constData;

    var Block = function(blockContainerThis, type , blockData) {

        var blockCodeLineType = type;
        if ( blockCodeLineType == BLOCK_CODELINE_TYPE.CLASS ) {
            var classNum = blockContainerThis.getClassNum();
            blockContainerThis.addClassNum();
        }
        if ( blockCodeLineType == BLOCK_CODELINE_TYPE.DEF) {
            var defNum = blockContainerThis.getDefNum();
            blockContainerThis.addDefNum();
        }
        if ( blockCodeLineType == BLOCK_CODELINE_TYPE.FOR ) {
            var forNum = blockContainerThis.getForNum();
            blockContainerThis.addForNum();
        }

        this.state = {
            type
            , blockType: BLOCK_TYPE.BLOCK
            , blockName: STR_NULL
            , opacity: 1
            
            , isLowerDepthChild: false
            , isRootBlock: false
            
            , isClicked: false
            , isCtrlPressed: false
            , isMoved: false
            , isNowMoved: false
            , isCodeLineDowned: false

            , uuid: vpCommon.getUUID()
            , direction: BLOCK_DIRECTION.ROOT
            , depth: 0
            , tempBlockLeftHolderHeight: 0
            , blockNumber: 0
            , width: 0
            , blockHeaderWidth: 0
            , blockCodeLineWidth: 0
            , variableIndex: 0

            , codeLine: STR_NULL
            , nextBlockUUIDList: []
            , optionState: {
               
                className: `vpClass${classNum}`
                , parentClassName: STR_NULL

                , classInParamList: [STR_NULL]
              
                , defName: `vpFunc${defNum}`
                , defInParamList: []
                , defReturnType: DEF_BLOCK_ARG4_TYPE.NONE

                , ifCodeLine: `('__home__' == '__main__')`
                , ifConditionList: [
                     {
                        arg1: ''
                        , arg2: ''
                        , arg3: ''
                        , arg4: ''
                        , arg5: ''
                        , arg6: ''
                        , codeLine: ''
                        , conditionType: IF_BLOCK_CONDITION_TYPE.ARG
                    }
                ]
                , elifList: []
              
                , elifConditionList: [
                    {
                        arg1: ''
                        , arg2: ''
                        , arg3: ''
                        , arg4: ''
                        , arg5: ''
                        , arg6: ''
                        , codeLine: ''
                        , conditionType: IF_BLOCK_CONDITION_TYPE.ARG
                    }
                ]
             
                , isIfElse: false
        
                , forCodeLine: `vp_i${forNum} in range(10)`
                , forParam: {
                    arg1: ''
                    , arg2: ''
                    , arg3: FOR_BLOCK_ARG3_TYPE.INPUT_STR
                    , arg4: ''
                    , arg5: ''
                    , arg6: ''
                    , arg7: ''

                    , arg3InputStr: ''
                    , arg3Default: ''
                }
                , forBlockOptionType: 'for'
                , isForElse: false
                , listforReturnVar: ''
                , listforPrevExpression: ``
                , listforConditionList: [
                    {  
                        arg1: ``
                        , arg2: ''
                        , arg3: FOR_BLOCK_ARG3_TYPE.INPUT_STR
                        , arg4: ''
                        , arg5: ''
                        , arg6: ''
                        , arg7: ''
       
                        , arg10: 'none'
                        , arg11: ``
                        , arg12: ''
                        , arg13: ``
                        , arg14: ''
                        , arg15: ``

                        , arg3InputStr: ''
                        , arg3Default: ''

                        , arg10InputStr: ''
                    }
                ]
                
                , whileCodeLine: 'False'
                , whileArgs: {
                    arg1: ''
                    , arg2: 'none'
                    , arg3: ''
                    , arg4: ''
                    , arg5: ''
                    , arg6: ''
                    , arg7: ''
                }
                , whileConditionList: [
                    {
                        arg1: ''
                        , arg2: ''
                        , arg3: ''
                        , arg4: ''
                        , arg5: ''
                        , arg6: ''
                        // , codeLine: ''
                        // , conditionType: IF_BLOCK_CONDITION_TYPE.ARG
                    }
                ]
                , whileBlockOptionType: 'condition'

                , exceptList: []
                , exceptConditionList: [
                    {
                        arg1: ``
                        , arg2: `none`
                        , arg3: ``
                        , codeLine: ''
                        , conditionType: IF_BLOCK_CONDITION_TYPE.ARG
                    }
                ]
                , finally: {
                    isFinally: false
                }
         
                ,baseImportList: [
                    baseImportNumpy = {
                        isImport: false
                        , baseImportName: 'numpy' 
                        , baseAcronyms: 'np' 
                    }   
                    , baseImportPandas = {
                        isImport: false
                        , baseImportName: 'pandas' 
                        , baseAcronyms: 'pd' 
                    }
                    , baseImportMatplotlib = {
                        isImport: false
                        , baseImportName: 'matplotlib.pyplot' 
                        , baseAcronyms: 'plt' 
                    }
                    , baseImportSeaborn = {
                        isImport: false
                        , baseImportName: 'seaborn' 
                        , baseAcronyms: 'sns' 
                    }
                    , baseImportOs = {
                        isImport: false
                        , baseImportName: 'os' 
                        , baseAcronyms: 'os' 
                    }
                    , baseImportSys = {
                        isImport: false
                        , baseImportName: 'sys' 
                        , baseAcronyms: 'sys' 
                    }
                    , baseImportTime = {
                        isImport: false
                        , baseImportName: 'time' 
                        , baseAcronyms: 'time' 
                    }
                    , baseImportDatetime = {
                        isImport: false
                        , baseImportName: 'datetime' 
                        , baseAcronyms: 'datetime' 
                    }
                    , baseImportRandom = {
                        isImport: false
                        , baseImportName: 'random' 
                        , baseAcronyms: 'random' 
                    }
                    , baseImportMath = {
                        isImport: false
                        , baseImportName: 'math' 
                        , baseAcronyms: 'math' 
                    }
                ]
                , customImportList: []
                , isBaseImportPage: true
              
                , lambdaArg1: ''
                , lambdaArg2List: [
                 
                ]
                , lambdaArg2m_List: [
                 
                ]
                , lambdaArg3: STR_NULL
                , lambdaArg4List: [
                    
                ]
                , elifCodeLine: STR_NULL
          
                , exceptCodeLine: ''
          
                , returnOutParamList: []
            
                , breakCodeLine: STR_BREAK
            
                , continueCodeLine: STR_CONTINUE
           
                , passCodeLine: STR_PASS
              
                , propertyCodeLine: STR_NULL
              
                , customCodeLine: STR_NULL
                
                , commentLine: STR_NULL
            }
        }


        this.nextBlockList = [];
        this.blockContainerThis = blockContainerThis;

        /** dom */
        this.rootDom = null;
        this.rootInnerDom = null;
        this.rootHeaderDom = null;
        this.containerDom = null;
        this.blockLeftHolderDom = null;
        this.blockNumInfoDom = null;
        this.depthInfoDom = null;
        this.blockLineNumberInfoDom = null;

        /** block */
        this.prevBlock = null;
        this.shadowBlock = null;
        this.firstIndentBlock = null;
        this.holderBlock = null;
        this.parentBlock = null;

        /** type block */
        this.ifElseBlock = null;
        this.forElseBlock = null;
        this.finallyBlock = null;
        this.lastElifBlock = null;
        this.lastChildBlock = null;
        this.propertyBlockFromDef = null;

        var name = MapTypeToName(type);
        this.setBlockName(name);
    
        var blockCodeLineType = this.getBlockCodeLineType();

        if (blockData) {
            this.state.optionState = blockData.blockOptionState;
            this.state.uuid = blockData.UUID;
        } 
        if (blockData == undefined) {
            /** class block일 경우 */
            if (blockCodeLineType == BLOCK_CODELINE_TYPE.CLASS) {
                var defBlock = this.blockContainerThis.createBlock(BLOCK_CODELINE_TYPE.DEF);
                defBlock.setState({
                    defName: '__init__'
                    , defInParamList:[{
                        arg3: STR_NULL
                        , arg4: DEF_BLOCK_ARG4_TYPE.NONE
                        , arg5: STR_NULL
                        , arg6: DEF_BLOCK_ARG6_TYPE.NONE
                    }]
                });
                defBlock.init();
                var defBlockMainDom = defBlock.getBlockMainDom();
                RenderHTMLDomColor(defBlock, defBlockMainDom);

                var holderBlock = this.blockContainerThis.createBlock(BLOCK_CODELINE_TYPE.HOLDER );
                this.setFirstIndentBlock(defBlock);

                this.setHolderBlock(holderBlock);
                holderBlock.setSupportingBlock(this);
                $(holderBlock.getBlockMainDom()).addClass(VP_BLOCK_BLOCKCODELINETYPE_CLASS_DEF);

                this.appendBlock(holderBlock, BLOCK_DIRECTION.DOWN);
                this.appendBlock(defBlock, BLOCK_DIRECTION.INDENT);

                $(this.getHolderBlock().getBlockMainDom()).css(STR_BACKGROUND_COLOR, COLOR_CLASS_DEF);

            /** def block일 경우 */
            } else if ( blockCodeLineType == BLOCK_CODELINE_TYPE.DEF) {
                
                var returnBlock = this.blockContainerThis.createBlock( BLOCK_CODELINE_TYPE.RETURN );
                var holderBlock = this.blockContainerThis.createBlock( BLOCK_CODELINE_TYPE.HOLDER );
                
                this.setHolderBlock(holderBlock);
                this.setFirstIndentBlock(returnBlock);
                holderBlock.setSupportingBlock(this);
                $(holderBlock.getBlockMainDom()).addClass(VP_BLOCK_BLOCKCODELINETYPE_CLASS_DEF);
                this.appendBlock(holderBlock, BLOCK_DIRECTION.DOWN);
                this.appendBlock(returnBlock, BLOCK_DIRECTION.INDENT);

                $(this.getHolderBlock().getBlockMainDom()).css(STR_BACKGROUND_COLOR, COLOR_CLASS_DEF);

            /** if, for, while, try block일 경우 */
            } else if ( blockCodeLineType == BLOCK_CODELINE_TYPE.IF 
                        || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR 
                        || blockCodeLineType == BLOCK_CODELINE_TYPE.WHILE 
                        || blockCodeLineType == BLOCK_CODELINE_TYPE.TRY ) {

                var passBlock = this.blockContainerThis.createBlock( BLOCK_CODELINE_TYPE.PASS);
                var holderBlock = this.blockContainerThis.createBlock( BLOCK_CODELINE_TYPE.HOLDER );
                
                this.setHolderBlock(holderBlock);
                this.setFirstIndentBlock(passBlock);
                holderBlock.setSupportingBlock(this);

                this.appendBlock(holderBlock, BLOCK_DIRECTION.DOWN);
                this.appendBlock(passBlock, BLOCK_DIRECTION.INDENT);

            /** else, elif, for else, except, finally block일 경우 */
            } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.ELSE 
                        || blockCodeLineType == BLOCK_CODELINE_TYPE.ELIF 
                        || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR_ELSE 
                        || blockCodeLineType == BLOCK_CODELINE_TYPE.EXCEPT 
                        || blockCodeLineType == BLOCK_CODELINE_TYPE.FINALLY ) {

                var passBlock = this.blockContainerThis.createBlock( BLOCK_CODELINE_TYPE.PASS);
                passBlock.renderSelectedBlockBorderColor();
                var holderBlock = this.blockContainerThis.createBlock( BLOCK_CODELINE_TYPE.HOLDER );
                
                this.setHolderBlock(holderBlock);
                this.setFirstIndentBlock(passBlock);
                holderBlock.setSupportingBlock(this);

                this.appendBlock(holderBlock, BLOCK_DIRECTION.DOWN);
                this.appendBlock(passBlock, BLOCK_DIRECTION.INDENT);

            } 
        }
        
        if (blockCodeLineType == BLOCK_CODELINE_TYPE.BREAK) {
            this.setState({
                customCodeLine: STR_BREAK
            });

        } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.CONTINUE) {
            this.setState({
                customCodeLine: STR_CONTINUE
            });
        } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.PASS) {
            this.setState({
                customCodeLine: STR_PASS
            });
        }

        this.blockContainerThis.addBlock(this);
        this.init();
        this.renderMyColor();
    }

    Block.prototype.init = function() {
        var blockContainerThis = this.getBlockContainerThis();
        var blockCodeLineType = this.getBlockCodeLineType();

        var blockMainDom = RenderBlockMainDom(this);
   
        if (blockCodeLineType == BLOCK_CODELINE_TYPE.HOLDER) {
            blockMainDom.classList.add(VP_CLASS_BLOCK_BOTTOM_HOLDER);
        }

    
        var mainInnerDom = RenderBlockMainInnerDom(this);
        var mainHeaderDom = RenderBlockMainHeaderDom(this);
        
        this.setBlockInnerDom(mainInnerDom);
        this.setBlockHeaderDom(mainHeaderDom);

        $(mainInnerDom).append(mainHeaderDom);          
        $(blockMainDom).append(mainInnerDom);
    

        var blockDepthInfoDom = $(`<span class='vp-block-depth-info'></span>`);
        var isShowDepth = blockContainerThis.getIsShowDepth();
        if ( isShowDepth == false ) {
            $(blockDepthInfoDom).css(STR_OPACITY, 0);
        }
 
        this.setBlockDepthInfoDom(blockDepthInfoDom);
        $(blockMainDom).append(blockDepthInfoDom);


        var blockLineNumberInfoDom = document.createElement(STR_SPAN);
        blockLineNumberInfoDom.classList.add(VP_CLASS_BLOCK_NUM_INFO);
        $(blockLineNumberInfoDom).append($(`<span class='vp-block-prefixnum-info'>
                                            </span>`));
        $(blockLineNumberInfoDom).append($(`<span class='vp-block-linenumber-info'>
                                        </span>`));                                          
        this.setBlockLineNumberInfoDom(blockLineNumberInfoDom);   
        $(blockMainDom).append(blockLineNumberInfoDom);


        var blockLeftHolderDom = $('<div class="vp-block-left-holder"></div>');
        var blockLeftHolderHeight = this.getTempBlockLeftHolderHeight();
        blockLeftHolderDom.css(STR_HEIGHT,`${blockLeftHolderHeight}${STR_PX}`);
        this.setBlockLeftHolderDom(blockLeftHolderDom);
        $(blockMainDom).append(blockLeftHolderDom);


        this.setBlockMainDom(blockMainDom);
        this.bindEventAll();
    }




    // ** --------------------------- Block을 삭제, 수정, 불러오기 혹은 주변 block과의 관계를 규정하는 메소드들 --------------------------- */

    Block.prototype.getPrevBlock = function() {
        return this.prevBlock
    }
    Block.prototype.setPrevBlock = function(prevBlock) {
        this.prevBlock = prevBlock;
    }
    Block.prototype.addNextBlockList = function(nextBlock) {
        this.nextBlockList = [ ...this.nextBlockList, nextBlock]
    }
    Block.prototype.setNextBlockList = function(nextBlockList) {
        this.nextBlockList = nextBlockList;
    }
    Block.prototype.getNextBlockList = function() {
        return this.nextBlockList;
    }
    Block.prototype.setHolderBlock = function(holderBlock) {
        this.holderBlock = holderBlock;
    }
    Block.prototype.getHolderBlock = function() {
        return this.holderBlock;
    }
    Block.prototype.setSupportingBlock = function(supportingBlock) {
        this.supportingBlock = supportingBlock;
    }
    Block.prototype.getSupportingBlock = function() {
        return this.supportingBlock;
    }

    Block.prototype.setFirstIndentBlock = function(firstIndentBlock) {
        this.firstIndentBlock = firstIndentBlock;
    }
    Block.prototype.getFirstIndentBlock = function() {
        return this.firstIndentBlock;
    }

    /**
     *  this block의 논리적인 parent block을 set, get
     *  ex) else, elif의 parent block은 if
     */
    Block.prototype.setParentBlock = function(parentBlock) {
        this.parentBlock = parentBlock;
    }
    Block.prototype.getParentBlock = function() {
        return this.parentBlock;
    }

    Block.prototype.setPropertyBlockFromDef = function(propertyBlockFromDef) {
        this.propertyBlockFromDef = propertyBlockFromDef;
    }
    Block.prototype.getPropertyBlockFromDef = function() {
        return this.propertyBlockFromDef;
    }
    /**
     * if 블럭이 생성한 elifList 중에 가장 아래에 위치한 elif block을 set, get
     * @param {BLOCK} lastElifBlock 
     */
    Block.prototype.setLastElifBlock = function(lastElifBlock) {
        this.lastElifBlock = lastElifBlock;
    }
    Block.prototype.getLastElifBlock = function() {
        return this.lastElifBlock;
    }
    
    /**
     * @param { Block } lastChildBlock 
     */
    Block.prototype.setLastChildBlock = function(lastChildBlock) {
        this.lastChildBlock = lastChildBlock;
    }
    Block.prototype.getLastChildBlock = function() {
        return this.lastChildBlock;
    }
    /**
     * for 블럭의 forElse block을 set, get
     * @param {Block} forElseBlock 
     */
    Block.prototype.setForElseBlock = function(forElseBlock) {
        this.forElseBlock = forElseBlock;
    }
    Block.prototype.getForElseBlock = function() {
        return this.forElseBlock;
    }

    /** 현재 블럭 트리 구조속의 최상위 루트 block 가져오기 */
    Block.prototype.getRootBlock = function() {
        var rootBlock = null;

        // if (this.getDirection() == BLOCK_DIRECTION.ROOT) {
        //     rootBlock = this;
        //     return rootBlock;
        // }
        // console.log('this',this);
        if (this.getPrevBlock() == null) {
            rootBlock = this;
            return rootBlock;
        }

        var prevBlock = this.getPrevBlock();

        var iteration = 0;
        while (prevBlock != null) {
            /** FIXME: 무한루프 체크 */
            if (iteration > NUM_MAX_ITERATION) {
                console.log(ERROR_AB0002_INFINITE_LOOP);
                break;
            }
            iteration++;
            var _prevBlock = prevBlock.getPrevBlock();
            if (_prevBlock == null) {
                rootBlock = prevBlock;
                break;
            }
            prevBlock = _prevBlock;
        }

        if (iteration == 0) {
            rootBlock = this;
        }
        return rootBlock;
    }

    /** 현재 root 블럭부터 모든 자식 블럭리스트 들을 전부 가져온다 */
    Block.prototype.getRootToChildBlockList = function() {
        var rootBlock = this.getRootBlock();
        return rootBlock.getChildBlockList();
    }

    /** 현재 this 블럭부터 모든 자식 블럭리스트 들을 가져온다 */
    Block.prototype.getChildBlockList = function() {
        var nextBlockList = this.getNextBlockList();
        var stack = [];

        if (nextBlockList.length != 0) {
            stack.push(nextBlockList);
        }

        var childBlockList = [this];
        childBlockList = this._getChildBlockList(childBlockList, stack);
        return childBlockList;
    }

    /** 현재 root 블럭부터 하위 depth 자식 블럭리스트(동일 depth 블럭 제거) 들을 전부 가져온다 */
    Block.prototype.getRootToChildLowerDepthBlockList = function() {
        var rootBlock = this.getRootBlock();
        return rootBlock.getChildLowerDepthBlockList();
    }

    /** 현재 this 블럭부터 하위 depth 자식 블럭리스트(동일 depth 블럭 제거) 들을 전부 가져온다 */
    Block.prototype.getChildLowerDepthBlockList = function() {
        var nextBlockList = this.getNextBlockList();
        var stack = [];
        var lastChildBlock = null;
        /** indent 위치에 자식 블럭이 있는지 확인 
         *  indent 위치에 자식 블럭이 있어야 하위 depth 자식 블럭들을 가져올 수 있다.
        */
        if (nextBlockList.length != 0) {
            stack = this._pushFirstChildIndentBlock(stack, nextBlockList);
        }

        var childLowerDepthBlockList  = [this];

        /** bottom holder block이 있으면 추가 */
        var holderBlock = null;
        var blockCodeLineType = this.getBlockCodeLineType();
        if (IsCanHaveIndentBlock(blockCodeLineType)) {
            nextBlockList.some(block => {
                if (block.getDirection() == BLOCK_DIRECTION.DOWN) {
                    childLowerDepthBlockList.push(block);
                    lastChildBlock = holderBlock = block;
                    return true;
                }
            });
        } else {
            lastChildBlock = this;
        }
  
        // && holderBlock != null
        if ( ( blockCodeLineType == BLOCK_CODELINE_TYPE.IF
            || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR
               || blockCodeLineType == BLOCK_CODELINE_TYPE.TRY )
               && holderBlock != null) {

            var result = holderBlock.getElifBlockList(true);  
            var { elifList, 
                  lastChildBlock: _lastChildBlock } = result;
            if (_lastChildBlock !== null) {
                lastChildBlock = _lastChildBlock;
            }  
        
            childLowerDepthBlockList = this._getChildBlockList(childLowerDepthBlockList, stack);
            elifList.forEach(block => {
                childLowerDepthBlockList.push(block);
            });
            this.setLastChildBlock(lastChildBlock);
            return childLowerDepthBlockList;

        } else {
            this.setLastChildBlock(lastChildBlock);
            childLowerDepthBlockList = this._getChildBlockList(childLowerDepthBlockList, stack);
            return childLowerDepthBlockList;
        }
    }

    Block.prototype._pushFirstChildIndentBlock = function( stack, nextBlockList ) {
        var selectedBlock = null;
        nextBlockList.some(block => {
            if (block.getDirection() == BLOCK_DIRECTION.INDENT) {
                selectedBlock = block;
                stack.push(selectedBlock);
                return true;
            }
        });
        return stack;
    }

    /**
     * @private
     * @param {Array<Block>} travelBlockList 
     * @param {Array<Block>} stack 
     */
    Block.prototype._getChildBlockList = function(travelBlockList, stack) {
        var iteration = 0;
        var current;
        while (stack.length != 0) {
            current = stack.shift();
            /** FIXME: 무한루프 체크 */
            if (iteration > NUM_MAX_ITERATION) {
                console.log(ERROR_AB0002_INFINITE_LOOP);
                break;
            }
            iteration++;
            /** 배열 일 때 */
            if (Array.isArray(current)) {
                var currBlockList = current;
                stack = DestructureFromBlockArray(stack, currBlockList);
            /** 배열 이 아닐 때 */
            } else {
                var currBlock = current;
                travelBlockList.push(currBlock);
                var nextBlockList = currBlock.getNextBlockList();
                stack.unshift(nextBlockList);
            }
        }
        return travelBlockList;
    }
    
    /** 생성할 블럭이 6뎁스를 초과 할 경우 alert창을 띄워 막음 */
    Block.prototype.alertExceedDepth = function() {
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).find(VP_CLASS_PREFIX + VP_BLOCK).remove();
        vpCommon.renderAlertModal(STR_MSG_BLOCK_DEPTH_MUSH_NOT_EXCEED_6);
        this.resetOptionPage();
    }

    /** param으로 받아온 block을 this블럭의 자식으로 append. 
     *  FIXME: 대대적인 변경 필요
     *  @param {BLOCK} appendedBlock
     *  @param {BLOCK_DIRECTION} direction
     */
    Block.prototype.appendBlock = function(appendedBlock, direction, isBlank = false) {
        var thisBlock = this;
        /**
         * depth가 6초과할 경우 alert
         */
        var depth = thisBlock.calculateDepthAndGet();
        if ( (depth >= NUM_EXCEED_DEPTH && direction == BLOCK_DIRECTION.INDENT)
            || depth > NUM_EXCEED_DEPTH) {
            appendedBlock.alertExceedDepth();
            return;
        }

        var prevBlock = appendedBlock.getPrevBlock();
        /** 이동한 block을 내 위치에 다시 놓을 경우 */
        if ( prevBlock ) {
            if (prevBlock.getUUID() == thisBlock.getUUID()) {
                return;
            }
        }
        
        if (isBlank == true) {
            var blockContainerThis = thisBlock.getBlockContainerThis();
            var blankBlock = blockContainerThis.createBlock( BLOCK_CODELINE_TYPE.BLANK );
            thisBlock.appendBlock(blankBlock,direction);
            thisBlock = blankBlock;
            direction = BLOCK_DIRECTION.DOWN;
        }
 

        thisBlock._deleteNextBlockFromPrevBlock(appendedBlock);

        appendedBlock.getChildLowerDepthBlockList();
        var lastChildBlock = appendedBlock.getLastChildBlock();

        // 새로 들어온 block의 이전 블럭을 현재 this블럭으로 정함
        appendedBlock.setPrevBlock(thisBlock);
        var nextBlockList = thisBlock.getNextBlockList();
        // console.log('block direction down');
        if (direction == BLOCK_DIRECTION.DOWN) {
            /** Elif Else 블럭 일 경우  */
            if (appendedBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.ELIF
                || appendedBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.EXCEPT
                || appendedBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.ELSE
                || appendedBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.FOR_ELSE
                || appendedBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.FINALLY ) {
                if (nextBlockList.length != 0) {
                    var getChildBlockList = appendedBlock.getChildBlockList();
                    getChildBlockList[getChildBlockList.length - 1].setNextBlockList([...nextBlockList]);
                }
                nextBlockList.forEach(block => {
                    block.setPrevBlock(getChildBlockList[getChildBlockList.length - 1]);
                    return true;          
                });
                thisBlock.setNextBlockList([appendedBlock]);  
            
            } else {
                thisBlock._nextLastChildBlockSetPrevBlock(prevBlock, appendedBlock, lastChildBlock);
                if (lastChildBlock != null) {
                    if (nextBlockList.length != 0) {
                        lastChildBlock.setNextBlockList([...nextBlockList]);
                    }
            
                    nextBlockList.forEach(block => {
                        block.setPrevBlock(lastChildBlock);
                        return true;          
                    });
                }
                thisBlock.setNextBlockList([appendedBlock]);  
            }
        // console.log('block direction indent');
        } else {
            thisBlock._nextLastChildBlockSetPrevBlock(prevBlock, appendedBlock, lastChildBlock);

            nextBlockList.some((nextBlock, index ) => {
                if (nextBlock.getDirection() == direction) {
                    // 새로 들어온 block이 기존에 자리잡고 있던 블록을 자식으로 append
                    nextBlock.setDirection(BLOCK_DIRECTION.DOWN);
                    lastChildBlock.addNextBlockList(nextBlock);
                    nextBlock.setPrevBlock(lastChildBlock);
                    nextBlockList.splice(index, 1);
                    return true;
                }
            });
            thisBlock.addNextBlockList(appendedBlock);
        }
        
        appendedBlock.setDirection(direction);
    }

    Block.prototype._nextLastChildBlockSetPrevBlock = function(prevBlock, appendedBlock, lastChildBlock) {
        var nextLastChildBlock = null;
        if (lastChildBlock != null && prevBlock != null) {
            lastChildBlock.getNextBlockList().some( (block,index) => {
                if ( block.getDirection() == BLOCK_DIRECTION.DOWN) {
                    nextLastChildBlock = block;
                    
                    nextLastChildBlock.setDirection( appendedBlock.getDirection() );
                    nextLastChildBlock.setPrevBlock(prevBlock);
                    prevBlock.addNextBlockList(nextLastChildBlock);
                    lastChildBlock.getNextBlockList().splice(index, 1);
                    return true;
                }
            });
        }
    }

    /**shadow block을 get */
    Block.prototype.getShadowBlock = function() {
        return this.shadowBlock;
    }
    /**
     * shadow block을 set 
     * @param {BLOCK} shadowBlock
     */
    Block.prototype.setShadowBlock = function(shadowBlock) {
        this.shadowBlock = shadowBlock;
    }

    /** 자식 블럭 리스트들 모두 제거 */
    Block.prototype.deleteBlock = function() {
        this._deleteNextBlockFromPrevBlock();
        /**  */
        var thisNextBlockDataList = this.getNextBlockList();
        var stack = [];
        
        if (thisNextBlockDataList.length != 0) {
            stack.push(thisNextBlockDataList);
        }

        var iteration = 0;
        var current;
        while (stack.length != 0) {
            /** FIXME: 무한루프 체크 */
            if (iteration > NUM_MAX_ITERATION) {
                console.log(ERROR_AB0002_INFINITE_LOOP);
                break;
            }
            
            current = stack.pop();
            /** 배열 일 때 */
            if (Array.isArray(current)) {
                current.forEach(block => {
                    stack.push(block);
                });
            /** 배열이 아닐 때 */
            } else {
                current.deleteBlock();
            }
        }

        this._deleteBlockDomAndData();
    }
    /**
     * 하위 depth block들을 지운다
     */
    Block.prototype.deleteLowerDepthChildBlocks = function() {
        var thisBlock = this;
        var blockContainerThis = this.getBlockContainerThis();


        /**
         *  만약 root 블럭일 경우 */
        if ( this.getPrevBlock() == null) {
            this.setDirection(BLOCK_DIRECTION.NONE);
            // console.log('root 블럭 삭제');
            var lastChildBlock = this.getLastChildBlock();
            var nextBlockList = lastChildBlock.getNextBlockList();
            lastChildBlock.setNextBlockList([]);
            nextBlockList.some(nextBlock => {
                nextBlock.setPrevBlock(null);
                nextBlock.setDirection(BLOCK_DIRECTION.ROOT);
            });

            if (blockContainerThis.getBlockList().length == 0) {
                var _containerDom = blockContainerThis.getBlockContainerDom();
                $(_containerDom).empty();
                $(_containerDom).remove();
            };
            this._deleteBlockDomAndData();

            var childLowerDepthBlockList = this.getChildLowerDepthBlockList();
            childLowerDepthBlockList.forEach(block => {
                block._deleteBlockDomAndData();
            });

            blockContainerThis.calculateDepthFromRootBlockAndSetDepth();
            blockContainerThis.reRenderBlockList();
            blockContainerThis.renderBlockLineNumberInfoDom(true);
            return;
        }

        // console.log('블럭 삭제');
        this._deleteNextBlockFromPrevBlock();

        var prevBlock = this.getPrevBlock();
        
        var deletedBlockDirection = this.getDirection();
        var childLowerDepthBlockList = this.getChildLowerDepthBlockList();

        var lastChildBlock = this.getLastChildBlock();

        if (lastChildBlock != null) {
            var nextBlockList = lastChildBlock.getNextBlockList();
            nextBlockList.some(nextBlock => {
                if (nextBlock) {
                    nextBlock.setDirection(deletedBlockDirection);
                    prevBlock.addNextBlockList(nextBlock);
                    nextBlock.setPrevBlock(prevBlock);
                    return true;
                }
            });
        }
        
        this._deleteBlockDomAndData();
        childLowerDepthBlockList.forEach(block => {
            block._deleteBlockDomAndData();
        });
        blockContainerThis.calculateDepthFromRootBlockAndSetDepth();
    }
    
    Block.prototype._deleteNextBlockFromPrevBlock = function(thatBlock) {
        var prevBlock = this.getPrevBlock();
        var block = this;
        
        if ( thatBlock ) {
            prevBlock =  thatBlock.getPrevBlock();
            block = thatBlock;
        }

        if ( prevBlock ) {
            var nextBlockList = prevBlock.getNextBlockList();
            nextBlockList.some(( nextBlockBlock, index) => {
                if (nextBlockBlock.getUUID() == block.getUUID()) {
                    nextBlockList.splice(index, 1)
                    return true;
                }
            });
        }
    }

    /** 
     *  blockContainer의 blockList에서 block 삭제
     */
    Block.prototype._deleteBlockDomAndData = function() {
    
        var blockMainDom = this.getBlockMainDom();
        $(blockMainDom).remove();
        $(blockMainDom).empty();

        /** blockContainer에서 block 데이터 삭제 제거 */
        var blockContainerThis = this.getBlockContainerThis();
        var blockUuid = this.getUUID(); 
        blockContainerThis.deleteBlock(blockUuid);
    }
    // ** --------------------------- Block dom 관련 메소드들 --------------------------- */

    Block.prototype.getBlockMainDom = function() {
        return this.rootDom;
    }
    Block.prototype.setBlockMainDom = function(rootDom) {
        this.rootDom = rootDom;
    }

    Block.prototype.getBlockInnerDom = function() {
        return this.rootInnerDom;
    }
    Block.prototype.setBlockInnerDom = function(rootInnerDom) {
        this.rootInnerDom = rootInnerDom;
    }

    Block.prototype.getBlockHeaderDom = function() {
        return this.rootHeaderDom;
    }
    Block.prototype.setBlockHeaderDom = function(rootHeaderDom) {
        this.rootHeaderDom = rootHeaderDom;
    }

    Block.prototype.setBlockLeftHolderDom = function(blockLeftHolderDom) {
        this.blockLeftHolderDom = blockLeftHolderDom;
    }
    Block.prototype.getBlockLeftHolderDom = function() {
        return this.blockLeftHolderDom;
    }

    Block.prototype.setBlockDepthInfoDom = function(depthInfoDom) {
        this.depthInfoDom = depthInfoDom;
    }
    Block.prototype.getBlockDepthInfoDom = function() {
        return this.depthInfoDom;
    }

    Block.prototype.setBlockLineNumberInfoDom = function(blockLineNumberInfoDom) {
        this.blockLineNumberInfoDom = blockLineNumberInfoDom;
    }
    Block.prototype.getBlockLineNumberInfoDom = function() {
        return this.blockLineNumberInfoDom;
    }
 
    Block.prototype.makeShadowDomList = function( shadowBlock, direction) {
        var thisBlock = this;
        var blockContainerThis = this.getBlockContainerThis();

        var indentPxNum = 0;
        var depth = thisBlock.getDepth();
        while (depth-- != 0) {
            indentPxNum += NUM_INDENT_DEPTH_PX;
        }
        if (direction == BLOCK_DIRECTION.INDENT) {
            indentPxNum += NUM_INDENT_DEPTH_PX;
        }

        var shadowDom = shadowBlock.getBlockMainDom();
        $(shadowDom).css(STR_MARGIN_LEFT, indentPxNum + STR_PX);
        $(shadowDom).css(STR_DISPLAY,STR_BLOCK);
        $(shadowDom).addClass(VP_CLASS_SELECTED_SHADOWBLOCK);
        shadowBlock.setSelectBlock(this);

        var containerDom = blockContainerThis.getBlockContainerDom();
        containerDom.insertBefore(shadowDom, thisBlock.getBlockMainDom().nextSibling);
    }

    /** 현재 root 블럭부터 하위 depth 자식 블럭리스트(동일 depth 블럭 제거) 들을 전부 가져오고,
     *  가져온 block들의 정보를 가지고 html dom을 만들어 return 한다. 
     */
    Block.prototype.makeChildLowerDepthBlockDomList = function(isShadowBlock) {
        var childBlockDomList = [];
        var rootDepth = 0;
        var $boardPage = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD));
        var $blockNewMainDom = null;
        var $moveChildListDom = null;
        var childBlockList = this.getChildLowerDepthBlockList();
        childBlockList.forEach((block, index) => {
            if (block == null) {
                return;
            }
            if (index == 0) {
                var depth = block.calculateDepthAndGet();
                rootDepth = depth;
                if (isShadowBlock == true) {
                    return;
                }
                /** 이동하는 block과 동일한 모양의 html tag 생성*/
                var blockNewMainDom = document.createElement(STR_DIV);
                blockNewMainDom.classList.add(VP_BLOCK);
                blockNewMainDom.classList.add(`vp-block-${block.getUUID()}`);
                blockNewMainDom = RenderHTMLDomColor(block, blockNewMainDom);
                $blockNewMainDom = $(blockNewMainDom);
                $blockNewMainDom.css(STR_POSITION, STR_ABSOLUTE);

                /** 이동하는 block의 header 생성 */
                var $mainInnerDom = $(`<div class='vp-block-inner'></div>`);
                var blockHeaderDom = RenderBlockMainHeaderDom(this);
                $mainInnerDom.append(blockHeaderDom);
                $blockNewMainDom.append( $mainInnerDom);

                // /** 이동하는 block에 자식 block의 dom을 생성해 append*/
                $moveChildListDom = $(`<div class='vp-block-stack'><div>`);
     
                $blockNewMainDom.append($moveChildListDom);

                /** 이동하는 block의 처음 block의 width 값 계산 */
                var rect = $(`.vp-block-${block.getUUID()}`)[0].getBoundingClientRect();
                $blockNewMainDom.css(STR_WIDTH, rect.width);
                $boardPage.append($blockNewMainDom);

                var blockLeftHolderDom = $('<div class="vp-block-left-holder"></div>');
                $blockNewMainDom.append(blockLeftHolderDom);
                return;

            } else {
                
                var blockMainDom = document.createElement(STR_DIV);
                blockMainDom.classList.add(VP_BLOCK);
                blockMainDom.classList.add(`vp-block-${block.getUUID()}`);
           
                var rect = $(`.vp-block-${block.getUUID()}`)[0].getBoundingClientRect();
                $(blockMainDom).css(STR_WIDTH, rect.width);
            
                var mainInnerDom = RenderBlockMainInnerDom(block);
                var mainHeaderDom = RenderBlockMainHeaderDom(block);

                $(mainInnerDom).append(mainHeaderDom);
                $(blockMainDom).append(mainInnerDom);

                var blockLeftHolderDom = $('<div class="vp-block-left-holder"></div>');
           
                blockMainDom = RenderHTMLDomColor(block, blockMainDom);
                blockLeftHolderDom = RenderHTMLDomColor(block, blockLeftHolderDom);
                $(blockMainDom).append(blockLeftHolderDom);

                if (block.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.HOLDER) {
                    $(blockMainDom).addClass(VP_CLASS_BLOCK_BOTTOM_HOLDER);
                    $(blockMainDom).css(STR_MARGIN_TOP, 0);
                    $(blockMainDom).css(STR_OPACITY, 10);
                }

                var depth = block.calculateDepthAndGet();
                var indentPxNum = 0;
                while (depth-- != 0) {
                    indentPxNum += NUM_INDENT_DEPTH_PX;
                }
                indentPxNum -= rootDepth * NUM_INDENT_DEPTH_PX;
         
                $(blockMainDom).css(STR_MARGIN_LEFT, indentPxNum + STR_PX);
                childBlockDomList.push(blockMainDom);

            }
        });
        

        if (isShadowBlock == false) {
            var $frag = $(document.createDocumentFragment());
            childBlockDomList.forEach(childDom => {
                $frag.append(childDom);
            });
            $moveChildListDom.append($frag);
        }
        if (isShadowBlock === true) {
            return childBlockDomList;
        } else {
            return {
                $moveChildListDom, $blockNewMainDom
            }
        }
    }

    /** block main dom의 width, height 값을 가져온다 */
    Block.prototype.getBlockMainDomPosition = function() {
        var blockMainDom = this.getBlockMainDom();
        var clientRect = $(blockMainDom)[0].getBoundingClientRect();
        return clientRect;
    }

    // ** --------------------------- Block 멤버변수의 set, get 관련 메소드들 --------------------------- */
    Block.prototype.setDepth = function(depth) {
        // this.setState({
        //     depth: depth
        // });
        this.state.depth = depth;
    }

    Block.prototype.getDepth = function() {
        return this.state.depth;
    }

    Block.prototype.getBlockCodeLineType = function() {
        return this.state.type;
    }

    Block.prototype.getBlockName = function() {
        return this.state.blockName;
    }
    Block.prototype.setBlockName = function(blockName) {
        this.setState({
            blockName
        });
    }
    Block.prototype.getUUID = function() {
        return this.state.uuid;
    }
    Block.prototype.setUUID = function(uuid) {
        this.setState({
            uuid
        });
    }
    /**
     * @param {ENUM} direction INDENT OR DOWN
     */
    Block.prototype.setDirection = function(direction) {
        this.setState({
            direction
        })
    }
    Block.prototype.getDirection = function() {
        return this.state.direction;
    }

    Block.prototype.getNextBlockUUIDList = function() {
        return this.state.nextBlockUUIDList;
    }
    Block.prototype.setNextBlockUUIDList = function(nextBlockUUIDList) {
        this.setState({
            nextBlockUUIDList
        });
    }

    Block.prototype.getBlockContainerThis = function() {
        return this.blockContainerThis;
    }

    /**
     *  순간 순간 임시로 변하는 left holder height
     */
    Block.prototype.getTempBlockLeftHolderHeight = function() {
        return this.state.tempBlockLeftHolderHeight;
    }
    
    Block.prototype.setTempBlockLeftHolderHeight = function(tempBlockLeftHolderHeight) {
        this.setState({
            tempBlockLeftHolderHeight
        });
    }

    Block.prototype.setIsClicked = function(isClicked) {
        this.setState({
            isClicked
        });
    }

    Block.prototype.getIsClicked = function() {
        return this.state.isClicked;
    }

    Block.prototype.getIsCtrlPressed = function() {
        return this.state.isCtrlPressed;
    }
    Block.prototype.setIsCtrlPressed = function(isCtrlPressed) {
        this.setState({
            isCtrlPressed
        });
    }

    Block.prototype.getIsMoved = function() {
        return this.state.isMoved;
    }
    Block.prototype.setIsMoved = function(isMoved) {
        this.setState({
            isMoved
        });
    }

    Block.prototype.getIsNowMoved = function() {
        return this.state.isNowMoved;
    }
    Block.prototype.setIsNowMoved = function(isNowMoved) {
        this.setState({
            isNowMoved
        });
    }

    Block.prototype.getIsCodeLineDowned = function() {
        return this.state.isCodeLineDowned;
    }
    Block.prototype.setIsCodeLineDowned = function(isCodeLineDowned) {
        this.setState({
            isCodeLineDowned
        });
    }

    /**  variableIndex을 set, get, add 
     * 
     */
    Block.prototype.setVariableIndex = function(variableIndex) {
        this.setState({
            variableIndex
        });
    }
    Block.prototype.getVariableIndex = function() {
        return this.state.variableIndex;
    }
    Block.prototype.addVariableIndex = function() {
        this.state.variableIndex++
        return this.state.variableIndex;
    }

    /** code를 생성하는 메소드 */
    Block.prototype.setCodeLineAndGet = function(indentString) {
        var thisBlock = this;
        var codeLine = STR_NULL;
        var blockName = this.getBlockName();

        if (indentString == undefined) {
            indentString = '';
        } 

        codeLine += indentString;

        var type = thisBlock.getBlockCodeLineType();
        switch (type) {
            //class
            case BLOCK_CODELINE_TYPE.CLASS: {
                codeLine += `${blockName.toLowerCase()}`;
                codeLine += STR_ONE_SPACE;
                codeLine += thisBlock.getState(STATE_className);
                codeLine += GenerateClassInParamList(thisBlock);

                break;
            }
            //def
            case BLOCK_CODELINE_TYPE.DEF: {
                codeLine += `${blockName.toLowerCase()}`;
                codeLine += STR_ONE_SPACE;
                codeLine += thisBlock.getState(STATE_defName);
                codeLine += GenerateDefInParamList(thisBlock);
            
                break;
            }
            //if
            case BLOCK_CODELINE_TYPE.IF: {
                codeLine += `${blockName.toLowerCase()}`;
                codeLine += STR_ONE_SPACE;
                codeLine += GenerateIfConditionList(thisBlock, BLOCK_CODELINE_TYPE.IF);
                codeLine += `:`;
                break;
            }
            //for
            case BLOCK_CODELINE_TYPE.FOR: {
                var forBlockOptionType = thisBlock.getState(STATE_forBlockOptionType);
                if (forBlockOptionType == FOR_BLOCK_TYPE.FOR) {
                    codeLine += `${blockName.toLowerCase()}`;
                    codeLine += STR_ONE_SPACE;
                    codeLine += GenerateForParam(thisBlock);
                    codeLine += `:`;
                } else {
                    codeLine += GenerateListforConditionList(thisBlock);
                }
             
                break;
            }
            //while
            case BLOCK_CODELINE_TYPE.WHILE: {
                codeLine += `${blockName.toLowerCase()}`;
                codeLine += STR_ONE_SPACE;
                codeLine +=  GenerateWhileConditionList(thisBlock);
                codeLine += `:`;
                break;
            }
            /** import */
            case BLOCK_CODELINE_TYPE.IMPORT: {
                codeLine += GenerateImportList(thisBlock, indentString);
                break;
            }
            /** api */
            case BLOCK_CODELINE_TYPE.API: {
                break;
            }
            /** try */
            case BLOCK_CODELINE_TYPE.TRY: {
                codeLine += `${blockName.toLowerCase()}:`;
                break;
            }
            /** return */
            case BLOCK_CODELINE_TYPE.RETURN: {
                codeLine += `${blockName.toLowerCase()} `;
                codeLine += GenerateReturnOutParamList(thisBlock);

                break;
            }

            /** break */
            case BLOCK_CODELINE_TYPE.BREAK: {
                codeLine += MapNewLineStrToSpacebar(thisBlock.getState(STATE_customCodeLine), indentString);
                break;
            }
            /** continue */
            case BLOCK_CODELINE_TYPE.CONTINUE: {
                codeLine += MapNewLineStrToSpacebar(thisBlock.getState(STATE_customCodeLine), indentString);
                break;
            }
            /** pass */
            case BLOCK_CODELINE_TYPE.PASS: {
                codeLine += MapNewLineStrToSpacebar(thisBlock.getState(STATE_customCodeLine), indentString);
                break;
            }
   
            /** elif */
            case BLOCK_CODELINE_TYPE.ELIF: {
                codeLine += `${blockName.toLowerCase()}`;
                codeLine += STR_ONE_SPACE;
                codeLine += GenerateIfConditionList(thisBlock,  BLOCK_CODELINE_TYPE.ELIF);
                codeLine += `:`;
                break;
            }
            /** else */
            case BLOCK_CODELINE_TYPE.ELSE: {
                codeLine += `${blockName.toLowerCase()}:`;
                break;
            }
            /** for else */
            case BLOCK_CODELINE_TYPE.FOR_ELSE: {
                codeLine += `${blockName.toLowerCase()}:`;
                break;
            }
            /** except */
            case BLOCK_CODELINE_TYPE.EXCEPT: {
                codeLine += `${blockName.toLowerCase()}`;
                codeLine += STR_ONE_SPACE;
                codeLine += GenerateExceptConditionList(thisBlock);
                codeLine += `:`;
                break;
            }
            /** finally */
            case BLOCK_CODELINE_TYPE.FINALLY: {
                codeLine += `${blockName.toLowerCase()}:`;
                break;
            }
            /** code */
            case BLOCK_CODELINE_TYPE.CODE: {
                codeLine += MapNewLineStrToSpacebar(thisBlock.getState(STATE_customCodeLine), indentString);
                break;
            }
            case BLOCK_CODELINE_TYPE.PROPERTY: {
                codeLine += '@';
                codeLine += MapNewLineStrToSpacebar(thisBlock.getState(STATE_customCodeLine), indentString);
                break;
            }
            case BLOCK_CODELINE_TYPE.LAMBDA: {
                codeLine += GenerateLambdaParamList(thisBlock);
                break;
            }
            case BLOCK_CODELINE_TYPE.COMMENT: {
                codeLine += '#';
                codeLine += thisBlock.getState(STATE_customCodeLine).replace(/(\r\n\t|\n|\r\t)/gm,"\n#");
                break;
            }
            case BLOCK_CODELINE_TYPE.PRINT: {
                codeLine += `${blockName.toLowerCase()}`;
                codeLine += `(`;
                codeLine += thisBlock.getState(STATE_customCodeLine).replace(/(\r\n\t|\n|\r\t)/gm,",");
                codeLine += `)`;
                break;
            }
        }
        this.state.codeLine = codeLine;
        return codeLine;
    }
    Block.prototype.getCodeLine = function() {
        return this.state.codeLine;
    }

    /**
     * block의 depth를 계산하고 depth 를 가져오는 함수
     */
    Block.prototype.calculateDepthAndGet = function() {
        var depth = 0;
        var currBlock = this;
        var direction = this.getDirection();

        var iteration = 0;
        var prevBlock = currBlock;
        while (prevBlock.getPrevBlock() != null) {
            prevBlock = prevBlock.getPrevBlock();
            if (iteration > NUM_MAX_ITERATION) {
                console.log(ERROR_AB0002_INFINITE_LOOP);
                break;
            }
            iteration++;
            
            if (direction == BLOCK_DIRECTION.INDENT
                && prevBlock.getDirection() != BLOCK_DIRECTION.DOWN ) {
                    depth++;
            } else {
                if (prevBlock.getDirection() == BLOCK_DIRECTION.INDENT) {
                    depth++;
                } 
            }
        }
     
        return depth;
    }

    /**
     * block의 left holder의 height를 계산하고 height를 set
     */
    Block.prototype.calculateLeftHolderHeightAndSet = function() {
        var blockCodeLineType = this.getBlockCodeLineType();
        var blockHeight = 0;
        if (blockCodeLineType == BLOCK_CODELINE_TYPE.CLASS 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.DEF) {
            blockHeight += NUM_BLOCK_BOTTOM_HOLDER_HEIGHT;
        }

        var childBlockList = this.getChildLowerDepthBlockList();
        childBlockList.forEach(childBlock => {
            if (childBlock == null) {
                return;
            }
            
            if ( childBlock.getBlockCodeLineType() !== BLOCK_CODELINE_TYPE.HOLDER ) {
                blockHeight += NUM_BLOCK_HEIGHT_PX;
            } else {
                blockHeight += NUM_BLOCK_BOTTOM_HOLDER_HEIGHT;
            }
        });

        this.setTempBlockLeftHolderHeight(blockHeight);
    }

    /**
     * block의 width를 set, get
     */
    Block.prototype.getWidth = function() {
        return this.state.width;
    }
    Block.prototype.setWidth = function(width) {
        this.setState({
            width
        });
    }

    /**
     * block의 blockHeaderWidth를 set, get
     */
    Block.prototype.getBlockHeaderWidth = function() {
        return this.state.blockHeaderWidth;
    }
    Block.prototype.setBlockHeaderWidth = function(blockHeaderWidth) {
        this.setState({
            blockHeaderWidth
        });
    }

    /**
     * block의 blockCodeLineWidth를 set, get
     */
    Block.prototype.getBlockCodeLineWidth = function() {
        return this.state.blockCodeLineWidth;
    }
    Block.prototype.setBlockCodeLineWidth = function(blockCodeLineWidth) {
        this.setState({
            blockCodeLineWidth
        });
    }

    Block.prototype.setBlockNumber = function(blockNumber) {
        this.blockNumber = blockNumber;
    }
    Block.prototype.getBlockNumber = function() {
        return this.blockNumber;
    }

    Block.prototype.setMovedBlockListOpacity = function(opacityNum) {
        var str = STR_NULL;
        if (opacityNum == 0) {
            str = STR_NONE;
        } else {
            str = STR_BLOCK;
        }

        var childBlockList = this.getChildLowerDepthBlockList();
        childBlockList.forEach(block => {
            var blockMainDom = block.getBlockMainDom();
            $(blockMainDom).css(STR_OPACITY, opacityNum);
            $(blockMainDom).css(STR_DISPLAY, str);
        });
    }
    // ** --------------------------- Block render 관련 메소드들 --------------------------- */

    Block.prototype.renderBlockLeftHolderHeight = function(px) {
        $( this.getBlockLeftHolderDom() ).css(STR_HEIGHT, px + STR_PX);
    }
    Block.prototype.resetBlockLeftHolderHeight = function() {
        $( this.getBlockLeftHolderDom() ).css(STR_HEIGHT, NUM_DEFAULT_BLOCK_LEFT_HOLDER_HEIGHT + STR_PX);
    }

    /** */
    Block.prototype.renderMyColor = function() {
        if (this.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.HOLDER) {
            var blockMainDom = this.getBlockMainDom();
            return;
        }
        var blockMainDom = this.getBlockMainDom();
        RenderHTMLDomColor(this, blockMainDom);
    }
  
    /** 
     * 
     * block에 칠해진 border를 reset하는 메소드
    */
    Block.prototype.renderResetColor = function() {

        var blockMainDom = this.getBlockMainDom();
        var blockCodeLineType = this.getBlockCodeLineType();
        /** class & def 블럭 */
        if ( blockCodeLineType == BLOCK_CODELINE_TYPE.CLASS 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.DEF) {
            $(blockMainDom).css(STR_BACKGROUND_COLOR, COLOR_CLASS_DEF);
        /** controls 블럭 */
        } else if ( blockCodeLineType == BLOCK_CODELINE_TYPE.IF 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR
            || blockCodeLineType == BLOCK_CODELINE_TYPE.WHILE 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.TRY
            || blockCodeLineType == BLOCK_CODELINE_TYPE.ELSE 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.ELIF
            || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR_ELSE 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.EXCEPT 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.FINALLY 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.LAMBDA
            || blockCodeLineType == BLOCK_CODELINE_TYPE.IMPORT
            || blockCodeLineType == BLOCK_CODELINE_TYPE.PROPERTY ) {
            $(blockMainDom).css(STR_BACKGROUND_COLOR, COLOR_CONTROL);
     
        }  
        else if (blockCodeLineType == BLOCK_CODELINE_TYPE.BLANK ) {
            $(blockMainDom).css(STR_BACKGROUND_COLOR, 'transparent');
        } 
        else if (blockCodeLineType == BLOCK_CODELINE_TYPE.HOLDER ) {

        } else {
            $(blockMainDom).css(STR_BACKGROUND_COLOR, COLOR_CODE);
        } 
    }
    /**
     * block 클릭시 block border 노란색으로 변경
     */
    Block.prototype.renderSelectedMainBlockBorderColor = function() {
        var blockContainerThis = this.getBlockContainerThis();
        var blockList = blockContainerThis.getBlockList();
        blockList.forEach(block => {
            $(block.getBlockMainDom()).css(STR_BORDER, '3px solid transparent');
        });

        $(this.getBlockMainDom()).css(STR_BORDER, '3px solid #F37704');
    }
    /**
     * block 클릭시 block border 노란색으로 변경
     */
    Block.prototype.renderSelectedBlockBorderColor = function() {
        var blockMainDom = this.getBlockMainDom();
        var blockCodeLineType = this.getBlockCodeLineType();
        /** class & def 블럭 */
        if ( blockCodeLineType == BLOCK_CODELINE_TYPE.CLASS 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.DEF) {

            $(blockMainDom).css(STR_BACKGROUND_COLOR, COLOR_CLASS_DEF_STRONG);
        /** controls 블럭 */
        } else if ( blockCodeLineType == BLOCK_CODELINE_TYPE.IF 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR
            || blockCodeLineType == BLOCK_CODELINE_TYPE.WHILE 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.TRY
            || blockCodeLineType == BLOCK_CODELINE_TYPE.ELSE 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.ELIF
            || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR_ELSE 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.EXCEPT 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.FINALLY 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.LAMBDA
            || blockCodeLineType == BLOCK_CODELINE_TYPE.IMPORT 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.PROPERTY   ) {
                
            $(blockMainDom).css(STR_BACKGROUND_COLOR, COLOR_CONTROL_STRONG);
        } 
        else if (blockCodeLineType == BLOCK_CODELINE_TYPE.BLANK ) {
            $(blockMainDom).css(STR_BACKGROUND_COLOR, 'transparent');
        } 
        else if (blockCodeLineType == BLOCK_CODELINE_TYPE.HOLDER ) {
 
        } else {
            $(blockMainDom).css(STR_BACKGROUND_COLOR, COLOR_CODE_STRONG);
        } 
    }

    Block.prototype.renderFontWeight700 = function() {
        $(this.getBlockLineNumberInfoDom).css(STR_FONT_WEIGHT, NUM_FONT_WEIGHT_700);
    }
    Block.prototype.renderFontWeight300 = function() {
        $(this.getBlockLineNumberInfoDom).css(STR_FONT_WEIGHT, NUM_FONT_WEIGHT_300);
    }

    /** elif block list를 가져온다
     * @param {boolean} isChildLowerDepthBlock
     * @return {Array<Block>}
     */
    Block.prototype.getElifBlockList = function(isChildLowerDepthBlock) {
        var thisBlock = this;
        var lastChildBlock = null;

        var elifList = [];
        var nextBlockList = thisBlock.getNextBlockList();
        var stack = [];
        if (nextBlockList.length != 0) {
            stack.push(nextBlockList);
        }

        var isBreak = false;
        var current;
        while (stack.length != 0) {
            current = stack.shift();
            /** 배열 일 때 */
            if (Array.isArray(current)) {
                current.forEach(block => {
                    var blockCodeLineType = block.getBlockCodeLineType();
                    var blockDirection = block.getDirection();
                    if ( blockDirection == BLOCK_DIRECTION.DOWN 
                        && ( blockCodeLineType == BLOCK_CODELINE_TYPE.IF
                            || blockCodeLineType == BLOCK_CODELINE_TYPE.TRY
                            || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR )) {
                        isBreak = true;
                    }

                    if ( blockDirection == BLOCK_DIRECTION.DOWN ) {
                        stack.push(block);
                        if (isChildLowerDepthBlock === true) {
                            if ( blockCodeLineType == BLOCK_CODELINE_TYPE.ELSE
                                || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR_ELSE
                                || blockCodeLineType == BLOCK_CODELINE_TYPE.FINALLY 
                                || blockCodeLineType == BLOCK_CODELINE_TYPE.ELIF
                                || blockCodeLineType == BLOCK_CODELINE_TYPE.EXCEPT ) {
                        
                                lastChildBlock = block.getHolderBlock();
                                elifList.push(lastChildBlock);

                                var elifOrElseChildLowerDepthBlockList = block.getChildLowerDepthBlockList();
                                elifOrElseChildLowerDepthBlockList.forEach(elifOrElseChildLowerDepthBlock => {
                                    elifList.push(elifOrElseChildLowerDepthBlock);
                                });
                            }
                        } else {
                            if ( blockCodeLineType == BLOCK_CODELINE_TYPE.ELIF
                                || blockCodeLineType == BLOCK_CODELINE_TYPE.EXCEPT ) {
                                elifList.push(block);    
                            }
                        }
                    }
                });

            } else {
                var currBlock = current;
                var nextBlockList = currBlock.getNextBlockList();
                stack.unshift(nextBlockList);
            }

            if (isBreak) {
                break;
            }
        }
        if (isChildLowerDepthBlock === true) {
            return {
                elifList
                , lastChildBlock
            }
        } else {
            return elifList;
        }
    }

    Block.prototype.resetOptionPage = function() {
        this.renderResetThisBlockBottomOption();
        this.renderResetBottomLowerDepthChildsBlockOption();
    }

    Block.prototype.renderResetThisBlockBottomOption = function() {
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_TAB_NAVIGATION_NODE_OPTION_TITLE_SAPN)).html(STR_OPTION);
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOTTOM_TAB_VIEW)).empty();
    }

    Block.prototype.renderResetBottomLowerDepthChildsBlockOption = function() {
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB_CHILDS_OPTION)).remove();
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOTTOM_OPTIONAL_TAB_VIEW)).empty();
    }

    /**
     * Block Type에 맵핑되는 Option을 Option tab에 렌더링하는 html 함수
     * @param {boolean} isChild true면 옵션 페이지에 자식 옵션으로 표시됨
     */
    Block.prototype.renderOptionPage = function(isChild) {
        var thisBlock = this;
        if (thisBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.HOLDER) {
            return;
        }

        var name = thisBlock.getBlockName();
        var capitalizeName = MakeFirstCharToUpperCase(name);

        var optionPageSelector = STR_NULL;

        if (isChild == true) {
            optionPageSelector = VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOTTOM_OPTIONAL_TAB_VIEW;
            var optionTitleDom = RenderOptionTitle(thisBlock);

            $(optionPageSelector).append(optionTitleDom);

        } else {
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_TAB_NAVIGATION_NODE_OPTION_TITLE_SAPN)).html(`${capitalizeName} ${STR_OPTION}s`);
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_TAB_NAVIGATION_NODE_OPTION_CHILDS_TOP_TITLE_SAPN)).html(`${capitalizeName} Child ${STR_OPTION}s`);
            optionPageSelector = VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOTTOM_TAB_VIEW;
            $(optionPageSelector).empty();
        }
        
        var blockCodeLineType = thisBlock.getBlockCodeLineType();
        switch(blockCodeLineType) {
            /** class */
            case BLOCK_CODELINE_TYPE.CLASS: {
                InitClassBlockOption(thisBlock, optionPageSelector);
                break;
            }
            /** def */
            case BLOCK_CODELINE_TYPE.DEF: {
                InitDefBlockOption(thisBlock, optionPageSelector);
                break;
            }

            /** if */
            case BLOCK_CODELINE_TYPE.IF: {
                InitIfBlockOption(thisBlock, optionPageSelector);
                break;
            }
            /** elif */
            case BLOCK_CODELINE_TYPE.ELIF: {
                InitElifBlockOption(thisBlock, optionPageSelector);
                break;
            }     
            /** else */
            case BLOCK_CODELINE_TYPE.ELSE: {
                InitElseBlockOption(thisBlock, optionPageSelector);
                break;
            }    

            /** for */
            case BLOCK_CODELINE_TYPE.FOR: {
                var forBlockOptionType = thisBlock.getState(STATE_forBlockOptionType);
                if (forBlockOptionType == FOR_BLOCK_TYPE.FOR) {
                    InitForBlockOption(thisBlock, optionPageSelector);
                } else {
                    InitListForBlockOption(thisBlock, optionPageSelector);
                }
                break;
            }
            /** while */
            case BLOCK_CODELINE_TYPE.WHILE: {
                InitWhileBlockOption(thisBlock, optionPageSelector);
                break;
            }

            /** Try */
            case BLOCK_CODELINE_TYPE.TRY: {
                InitTryBlockOption(thisBlock, optionPageSelector);
                break;
            }
            /** Except */
            case BLOCK_CODELINE_TYPE.EXCEPT: {
                InitExceptBlockOption(thisBlock, optionPageSelector);
                break;
            }   
            /** Return */
            case BLOCK_CODELINE_TYPE.RETURN : {
                InitReturnBlockOption(thisBlock, optionPageSelector);
                break;
            }

            /** Code block */
            case BLOCK_CODELINE_TYPE.CODE: {
                InitCodeBlockOption(thisBlock, optionPageSelector);
                break;
            }

            /** Break block */
            case BLOCK_CODELINE_TYPE.BREAK: {
                InitCodeBlockOption(thisBlock, optionPageSelector);
                break;
            }
       
            /** Continue block */
            case BLOCK_CODELINE_TYPE.CONTINUE: {
                InitCodeBlockOption(thisBlock, optionPageSelector);
                break;
            }
          
            /** Property block */
            case BLOCK_CODELINE_TYPE.PROPERTY: {
                InitCodeBlockOption(thisBlock, optionPageSelector);
                break;
            }
            /** Pass block */
            case BLOCK_CODELINE_TYPE.PASS:  {
                InitCodeBlockOption(thisBlock, optionPageSelector);
                break;
            }

            /** Lambda block */
            case BLOCK_CODELINE_TYPE.LAMBDA: {
                InitLambdaBlockOption(thisBlock, optionPageSelector);
                break;
            }
            /** Comment block */
            case BLOCK_CODELINE_TYPE.COMMENT: {
                InitCodeBlockOption(thisBlock, optionPageSelector);
                break;
            }

            /** Sample block */
            case BLOCK_CODELINE_TYPE.SAMPLE: {
                InitSampleBlockOption(thisBlock, optionPageSelector);
                break;
            }
            case BLOCK_CODELINE_TYPE.PRINT: {
                InitCodeBlockOption(thisBlock, optionPageSelector);
                break;
            }  
            case BLOCK_CODELINE_TYPE.API: {
                // InitApiBlockOption(thisBlock, optionPageSelector);
                break;
            }
            /** Import */
            case BLOCK_CODELINE_TYPE.IMPORT: {
                InitImportBlockOption(thisBlock, optionPageSelector);
                break;
            }
        }
    }

    // ** --------------------------- Block state 관련 메소드들 --------------------------- */
    Block.prototype.setState = function(newState) {
        this.state = ChangeOldToNewState(this.state, newState);
        this.consoleState();
        this.setCodeLineAndGet();
        this.setBlockTitle();
        // var blockContainerThis = this.getBlockContainerThis();
        // blockContainerThis.setAPIBlockMetadata();
    }

    /**특정 state Name 값을 가져오는 함수
        @param {string} stateKeyName
    */
    Block.prototype.getState = function(stateKeyName) {
        return FindStateValue(this.state, stateKeyName);
    }
    Block.prototype.getStateAll = function() {
        return this.state;
    }
    Block.prototype.consoleState = function() {
        // console.log(this.state);
    }

    /** 변경된 codeline state를 html title로 set */
    Block.prototype.setBlockTitle = function() {
        var codeLine = this.getCodeLine();

        var blockMainDom = this.getBlockMainDom();
        $(blockMainDom).attr(STR_TITLE,  codeLine);
    }

    Block.prototype.renderRemoveDom = function(blockOldMainDom, moveChildListDom) {

        $(blockOldMainDom).remove();
            
        $(moveChildListDom).remove();
        $(moveChildListDom).empty();
    }

    /** ---------------------------이벤트 함수 바인딩--------------------------- */
    Block.prototype.bindEventAll = function() {
        var blockCodeLineType = this.getBlockCodeLineType();
        // this.getPrevBlock() == null
        //     ||
        if ( blockCodeLineType == BLOCK_CODELINE_TYPE.ELIF
            || blockCodeLineType == BLOCK_CODELINE_TYPE.ELSE
            || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR_ELSE
            || blockCodeLineType == BLOCK_CODELINE_TYPE.EXCEPT
            || blockCodeLineType == BLOCK_CODELINE_TYPE.FINALLY ) {
            this.bindClickEvent();
            return;
        }
        this.bindClickEvent();
        this.bindDragEvent();
    }

    /**
     * TODO: 추후 개선해야 할 메소드 
     * @async
     * block drag시 발생하는 이벤트 메소드 
     */
    Block.prototype.bindDragEvent = function() {
        var thisBlock = this;
        
        var blockContainerThis = this.getBlockContainerThis();
        var blockCodeLineType = this.getBlockCodeLineType();

        var blockOldMainDom = this.getBlockMainDom();
        var x = 0;
        var y = 0;
  
        var shadowBlock = null;
        var nowMovedBlockList = [];
        var selectedBlock = null;
        var selectedBlockDirection = null;

        var currCursorX = 0;
        var currCursorY = 0;

        /** 제이쿼리 변수 */
        var $blockNewMainDom = null;
        var $blockOldMainDom = $(blockOldMainDom);
   
        var $moveChildListDom = null;
        var $boardPage = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD));
        var $shadowBlockMainDom = null;
        
        var isOnlyRootBlockAtBoard = false;
        var isCollision50perInner = true;
        $blockOldMainDom.draggable({ 
            addClass: 'vp-dragable-btn',
            revert: 'invalid',
            revertDuration: 200,
            containment: VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD,
            cursor: 'move', 
            distance: 10,
            start: (event, ui) => {
               
                /** board 초록색 border 색칠 */
                blockContainerThis.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.EDITOR);

                ( { $blockNewMainDom, $moveChildListDom }  = thisBlock.makeChildLowerDepthBlockDomList(false));
                /** 이동하는 하위 depth Block 들 opacity 0 */
                thisBlock.setMovedBlockListOpacity(0);

                /** 이동하는 하위 depth Block 들 isMoved true */
                nowMovedBlockList = thisBlock.getChildLowerDepthBlockList();
                nowMovedBlockList.forEach(block => {
                    block.setIsNowMoved(true);
                    block.setIsMoved(true);
                });
                blockContainerThis.setNowMovedBlockList(nowMovedBlockList);

                /** shadow block 생성 */
                var shadowChildBlockDomList = thisBlock.makeChildLowerDepthBlockDomList(true);
                shadowBlock = new ShadowBlock(blockContainerThis, blockCodeLineType, 
                                            shadowChildBlockDomList, thisBlock);
                $shadowBlockMainDom = $(shadowBlock.getBlockMainDom());
                $shadowBlockMainDom.css(STR_DISPLAY,STR_NONE);

                var containerDom = blockContainerThis.getBlockContainerDom();
                $(containerDom).append(shadowBlock.getBlockMainDom());

                var blockList = blockContainerThis.getBlockList();
                blockList.forEach(block => {
                    var holderBlock = block.getHolderBlock();
                    if ( holderBlock != null ) {
                        block.calculateLeftHolderHeightAndSet();
                        var distance = block.getTempBlockLeftHolderHeight();
                        $(block.getBlockLeftHolderDom()).css(STR_HEIGHT, distance);
                    }
                });
            },
            drag: async (event, ui) => {
                    /** 현재 drag하는 Block의 위치 구현 */
                    blockContainerThis.setEventClientY(event.clientY);
    
                    currCursorX = event.clientX; 
                    currCursorY = event.clientY; 
    
                    var scrollHeight =  blockContainerThis.getScrollHeight();
                    var maxWidth =  blockContainerThis.getMaxWidth();
 
                    /** 블럭 드래그시 
                     *  왼쪽 정렬  
                     */
                    x = currCursorX - $boardPage.offset().left;
                    y = currCursorY - ( $boardPage.offset().top - $boardPage.scrollTop() );
    
                    // if (x < 0) {
                    //     x = 0;
                    // }
                    /** 이동한 블럭들의 루트블럭 x좌표가 editor 화면의 maxWidth 이상 일때 */
                    if (x > maxWidth - $blockNewMainDom.width()) {
                        x = maxWidth - $blockNewMainDom.width();
                    }
                    /** 이동한 블럭들의 루트블럭 y좌표가 editor 화면의 maxHeight 이상 일때 */
                    if (y > scrollHeight - ( $moveChildListDom.height() + NUM_BLOCK_HEIGHT_PX ) ) {
                        y = scrollHeight - ( $moveChildListDom.height() + NUM_BLOCK_HEIGHT_PX );
                    }
                    /** 이동한 블럭들의 루트블럭 y좌표가 0 이하 일때 */
                    if (y < 0) {
                        y = 0;
                    }
    
                    $blockNewMainDom.css(STR_TOP, y + STR_PX);
                    $blockNewMainDom.css(STR_LEFT, x + STR_PX);
         
                    /** 블록 전체를 돌면서 drag하는 Block과 Editor위에 생성된 블록들과 충돌 작용  */
                    var blockList = blockContainerThis.getBlockList();
                    // for await ( var block of blockList ) {
                    blockList.forEach( async (block) => {
                        
                        /** 자기 자신인 블럭과는 충돌 금지 
                         *  혹은 자신의 하위 블럭과도 충돌 금지
                        */
                        if ( thisBlock.getUUID() == block.getUUID()
                            || block.getIsNowMoved() == true ) {
                            return;
                        }

                        /** 충돌할 block의 x,y, width, height를 가져온다 */
                        var { x: blockX, 
                              y: blockY, 
                              width: blockWidth, 
                              height: blockHeight } = block.getBlockMainDomPosition();

                        /** 블럭 충돌에서 벗어나는 로직 */
                        var blockLeftHolderHeight = block.getTempBlockLeftHolderHeight();
                        if ( (blockX > currCursorX 
                              || currCursorX > (blockX + blockWidth)
                              || blockY  > currCursorY 
                              || currCursorY > (blockY + blockHeight + blockHeight + blockHeight + blockLeftHolderHeight) ) ) {
                            block.renderBlockHolderShadow_2(STR_NONE);
                        }

                        /** 블럭 충돌 left holder shadow 생성 로직 */
                        if ( blockX < currCursorX
                            && currCursorX < (blockX + blockWidth)
                            && blockY  < currCursorY
                            && currCursorY < (blockY + blockHeight + blockHeight + blockLeftHolderHeight) ) {     
                            block.renderBlockHolderShadow_2(STR_BLOCK);

                            var holderBlock = block.getHolderBlock();
                            if ( holderBlock != null ) {
                                 block._renderBlockLeftHolderListHeight();
                            }
                        }

                        /** 블럭 충돌 로직 */  
                        if ( blockX < currCursorX
                                && currCursorX < (blockX + blockWidth + blockWidth)
                                && blockY  < currCursorY
                                && currCursorY < (blockY + blockHeight  + blockHeight) ) { 

                            if ( currCursorY < (blockY + blockHeight + blockHeight /1.5) )  {
                                // console.log('50% 이상');
                                isCollision50perInner = true;
                            } else {
                                // console.log('50% 이하');
                                isCollision50perInner = false;
                            }
                            var holderBlock = block.getHolderBlock();
                            if ( holderBlock != null ) {
                                block._renderBlockLeftHolderListHeight();
                            }

                            /** 충돌시 direction 설정
                             * direction은 DOWN,  INDENT
                             */
                            var holderBlock = block.getHolderBlock();
                            if ( holderBlock != null ) {
                                selectedBlockDirection = BLOCK_DIRECTION.INDENT;
                            } else {
                                selectedBlockDirection = BLOCK_DIRECTION.DOWN; 
                            }

                            block.makeShadowDomList( shadowBlock, selectedBlockDirection);
                        } else {
                            /** shadow 블록 생성하는 로직
                             * css class로 마크된 block을 selectedBlock에 저장 한다
                             */
                            if ( $shadowBlockMainDom.hasClass(VP_CLASS_SELECTED_SHADOWBLOCK) ) {
                                selectedBlock = shadowBlock.getSelectBlock();
                            }

                            var containerDom = blockContainerThis.getBlockContainerDom();
                            var containerDomRect = $(containerDom)[0].getBoundingClientRect();
                            var { x: containerDomX, 
                                  y: containerDomY, 
                                  width: containerDomWidth, 
                                  height: containerDomHeight } = containerDomRect;
            
                            /** board에 있는 어떠한 block에 닿았을 때 */
                            if ( containerDomX < event.clientX
                                && event.clientX < (containerDomX + containerDomWidth)
                                && containerDomY  < event.clientY
                                && event.clientY < (containerDomY + containerDomHeight) ) {  
                            
                            /** board에 있는 어떠한 block에도 닿지 않았을 때 */
                            } else {
                                /** shadow 블록 해제하는 로직
                                 * css class로 마크된 block을 selectedBlock에 저장 한다
                                 */
                                $shadowBlockMainDom.css(STR_DISPLAY,STR_NONE);
                                shadowBlock.setSelectBlock(null);
                                selectedBlock = null;
                            }
                        }
                    });
                }, 
                stop: function(event, ui) { 
                    // console.log('stop start');
                    
                    // 화면 밖으로 나갔을 때, 재조정
                    var maxWidth =  blockContainerThis.getMaxWidth();
                    var maxHeight =  blockContainerThis.getMaxHeight();
    
                    var isDisappeared = false;
                    /** 이동한 블럭들의 루트블럭 x좌표가 0 이하 일때 */
                    if (x < 0) {
                        x = 0;
                        isDisappeared = true;
                    }
                    /** 이동한 블럭들의 루트블럭 x좌표가 editor 화면의 maxWidth 이상 일때 */
                    if (x > maxWidth - $blockOldMainDom.width()) {
                        x = maxWidth - $blockOldMainDom.width();
                        isDisappeared = true;
                    }
                    /** 이동한 블럭들의 루트블럭 y좌표가 editor 화면의 maxHeight 이상 일때 */
                    if (y > maxHeight - ( $moveChildListDom.height() + NUM_BLOCK_HEIGHT_PX ) ) {
                        y = maxHeight - ( $moveChildListDom.height() + NUM_BLOCK_HEIGHT_PX );
    
                    }
                    /** 이동한 블럭들의 루트블럭 y좌표가 0 이하 일때 */
                    if (y < 0) {
                        y = 0;
                        isDisappeared = true;
                    }
    
                    selectedBlock = shadowBlock.getSelectBlock();
        
                    
                    /** 블록이 화면 밖으로 나갈경우, 나간 블럭 전부 삭제 */
                    if (isDisappeared == true && !selectedBlock) {
                        thisBlock.deleteLowerDepthChildBlocks();

                    /** 블록이 화면 밖으로 나가지 않고 연결되는 경우 */
                    } else {
                        var isConntected = true;
                        /** 어떤 블록의 DOWN이나 INDENT로 조립되지 않는 경우 */
                        if (!selectedBlock) {
                            /** 이동한 block이 rootblock일 경우 */
                            if ( thisBlock.getPrevBlock() == null ) {
                
          
                                isConntected = false;
                                selectedBlock = blockContainerThis.getRootToLastBottomBlock();

                                thisBlock._moveRootBlock();
                                thisBlock.setDirection(BLOCK_DIRECTION.DOWN);
                                
                            }
                            /** 이동한 block의 prevBlock이 rootblock일 경우 */
                            else if ( thisBlock.getPrevBlock().getUUID() == blockContainerThis.getRootBlock().getUUID() ) {
                                isConntected = false;
                                selectedBlock = blockContainerThis.getRootToLastBottomBlock();

                            /** 이동한 block의 prevBlock이 rootblock이 아닐 경우 */
                            } else {
                
                                isConntected = false;
                                var lastBottomBlock = blockContainerThis.getRootToLastBottomBlock();

                                /** 이동한 Block 하위에, Board에 놓여 있는 맨 마지막 Block이 포함되어 있는 경우 */
                                var isFinalBlock = thisBlock.getChildLowerDepthBlockList().some(block => {
                     
                                    if ( block.getUUID() == lastBottomBlock.getUUID() ) {
 
                                        if ( thisBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.IF
                                            || thisBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.FOR ) {
                                 
                                            var thisBlockDepth = thisBlock.getDepth();
                                            if (thisBlockDepth == 0) {
                                                while( ( lastBottomBlock.getBlockCodeLineType() != BLOCK_CODELINE_TYPE.IF ||
                                                         lastBottomBlock.getBlockCodeLineType() != BLOCK_CODELINE_TYPE.FOR )
                                                        && thisBlock.getUUID() != lastBottomBlock.getUUID() ) {
                                                    lastBottomBlock = lastBottomBlock.getPrevBlock();
                                                }
                                                selectedBlock = lastBottomBlock.getPrevBlock();
                                            } else {
                                                selectedBlock = lastBottomBlock;
                                            }
                                      
                                        } else if ( lastBottomBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.HOLDER ) {
                                            selectedBlock = lastBottomBlock.getPrevBlock().getPrevBlock();

                                        } else {
                                            selectedBlock = lastBottomBlock.getPrevBlock();
                                        }
                                        return true;
                                    }
                                });
                         
                                /** 이동하는 하위 depth Block 들이 
                                 *  board에 놓여있는 block들의 맨 마지막 위치에 있는 block이 아닐 경우
                                 */
                                if (isFinalBlock == false) {
                                    selectedBlock = lastBottomBlock;
                                }
                            }
                        }

                        /** 이동하는 하위 depth Block 들의 opacity 1로 변경 */
                        thisBlock.setMovedBlockListOpacity(1);

                        /** 어떤 블록의 DOWN이나 INDENT로 조립되지 않는 경우 */
                        if (isConntected == false) {
                            /** 움직인 블럭이 ROOT 블럭이고 움직인 블럭의 하위 depth 블럭이외의 board에 블럭이 없을 경우 */
                            isOnlyRootBlockAtBoard = thisBlock.getChildLowerDepthBlockList().some(block => {
                                if (selectedBlock.getUUID() == block.getUUID()) {
                                    return true;
                                }
                            });

                            if (isOnlyRootBlockAtBoard == false) {
                                // console.log('여기 1');
                                selectedBlock.appendBlock(thisBlock, BLOCK_DIRECTION.DOWN);
                            }
                           
                        /** 특정 블록의 DOWN이나 INDENT로 조립된 경우 */ 
                        } else {
                            /** 이동한 block이 rootblock일 경우 */
                            if ( thisBlock.getPrevBlock() == null ) {
                                thisBlock._moveRootBlock();
                            }
                            selectedBlock.appendBlock(thisBlock, selectedBlockDirection);

                            // if (isCollision50perInner == false) {
                              
                            //     selectedBlock.appendBlock(thisBlock, selectedBlockDirection);
                            // } else {
                            //     selectedBlock.appendBlock(thisBlock, selectedBlockDirection);
                            // }
                            // selectedBlock.appendBlock(thisBlock, selectedBlockDirection);
                        }
                    }

                    var rootBlockContainerDom = blockContainerThis.getBlockContainerDom();
                    $(rootBlockContainerDom).find(VP_CLASS_PREFIX + VP_CLASS_BLOCK_SHADOWBLOCK_CONTAINER).remove();

                    if (isOnlyRootBlockAtBoard == true) {
                        thisBlock.setDirection(BLOCK_DIRECTION.ROOT);
                    } 

                    thisBlock.renderRemoveDom($blockOldMainDom, $moveChildListDom);
                    $blockNewMainDom.remove();
                
                    blockContainerThis.calculateDepthFromRootBlockAndSetDepth();
           
                    blockContainerThis.bindCodeBlockInputFocus(thisBlock, blockCodeLineType);

                    blockContainerThis.reRenderBlockList();
                    blockContainerThis.renderBlockLineNumberInfoDom();
                
                    thisBlock.renderEditorScrollTop();

                    /** 모든 0 Depth Block 한칸 띄우기
                     *  모든 Block border color 리셋
                     *  모든 Block에서 생성된 shadow 지우기
                     */
                    var blockList = blockContainerThis.getBlockList();
                    blockList.forEach(block => {
                        block.renderBlockHolderShadow_2(STR_NONE);
                        block.renderCodeLineDowned();
                        block.renderResetColor();
                        block.renderFontWeight300();

                        $(block.getBlockMainDom()).find(VP_CLASS_PREFIX + VP_CLASS_BLOCK_DELETE_BTN).remove();
                        $(block.getBlockMainDom()).find(VP_CLASS_PREFIX + VP_CLASS_BLOCK_OPTION_BTN).remove();
                        $(block.getBlockMainDom()).find(VP_CLASS_PREFIX + 'vp-apiblock-elif-else-container-button').remove();
                    });
                    
                    thisBlock.renderSelectedMainBlockBorderColor();

                    /** 서브 버튼 생성 */
                    thisBlock.createSubButton();

                    /** 옵션 페이지 리셋  */
                    thisBlock.resetOptionPage();

                    /** 옵션 페이지 다시 오픈 */
                    blockContainerThis.setSelectedBlock(thisBlock);
                    blockContainerThis.renderBlockOptionTab();
                    thisBlock.renderOptionPage();

                    /** 자식 하위 Depth Block Border 색칠 */
                    var childLowerDepthBlockList = thisBlock.getChildLowerDepthBlockList();
                    childLowerDepthBlockList.forEach(block => {
                        block.renderSelectedBlockBorderColor();
                        block.renderFontWeight700();
                        block.setIsNowMoved(false);
                    });

     

                    nowMovedBlockList = [];
                    shadowBlock = null;
                }
            });
        // }
    }

    Block.prototype._moveRootBlock = function() {
        this.getChildLowerDepthBlockList();
        var lastChildBlock = this.getLastChildBlock();
        var nextBlockList = lastChildBlock.getNextBlockList();
        lastChildBlock.setNextBlockList([]);
        nextBlockList.some(nextBlock => {
            nextBlock.setPrevBlock(null);
            nextBlock.setDirection(BLOCK_DIRECTION.ROOT);
        });
    }
    Block.prototype.createSubButton = function() {

        var thisBlock = this;
        var blockContainerThis = thisBlock.getBlockContainerThis();
        var blockMainDom = thisBlock.getBlockMainDom();
        var blockCodeLineType = thisBlock.getBlockCodeLineType();

        // var runBtn = RenderRunBlockButton();
        var deleteBtn = RenderDeleteBlockButton();

        var elseOnOffStr = STR_NULL;
        if (thisBlock.getState(STATE_isIfElse) == true) {
            elseOnOffStr = 'off';
        } else {
            elseOnOffStr = 'on';
        }

        if (blockCodeLineType == BLOCK_CODELINE_TYPE.IF) {

            var containerButton = $(`<div class='${VP_CLASS_STYLE_FLEX_ROW_BETWEEN}
                                                  vp-apiblock-elif-else-container-button' 
                                          style='width:160px; right:0; position:absolute; margin-top: -36px;'>
                                        </div>`);
            var plusElifButton = $(`<div class='vp-apiblock-plus-elif-button'>+ elif</div>'`);
            var toggleElseButton = $(`<div class='vp-apiblock-toggle-else-button'> else ${elseOnOffStr} </div>`);
            containerButton.append(plusElifButton);
            containerButton.append(toggleElseButton);
            $(blockMainDom).append(containerButton);
            $(plusElifButton).click(function(plusElifEvent) {
                var selectedBlock = thisBlock.getLastElifBlock() || thisBlock;
                var newBlock = blockContainerThis.createBlock(BLOCK_CODELINE_TYPE.ELIF);
                thisBlock.setLastElifBlock(newBlock);

                selectedBlock.getHolderBlock().appendBlock(newBlock, BLOCK_DIRECTION.DOWN);

                var elifConditionCode = GenerateIfConditionList(newBlock, BLOCK_CODELINE_TYPE.ELIF);
                $(`.vp-block-header-${newBlock.getUUID()}`).html(elifConditionCode);
               
                // blockContainerThis.renderBlockOptionTab();
                blockContainerThis.reRenderBlockList();
                blockContainerThis.renderBlockLineNumberInfoDom(true);
                blockContainerThis.calculateDepthFromRootBlockAndSetDepth();
    
                newBlock.renderSelectedBlockBorderColor();
                plusElifEvent.stopPropagation();
            });
            $(toggleElseButton).click(function() {
                /** else가 존재하는 경우 -> else 삭제*/
                if (thisBlock.getState(STATE_isIfElse) == true) {
                    var elseBlock = thisBlock.ifElseBlock;
                    elseBlock.deleteLowerDepthChildBlocks();
                    thisBlock.ifElseBlock = null;
                    blockContainerThis.reRenderBlockList();
                    blockContainerThis.renderBlockLineNumberInfoDom(true);

                    thisBlock.setState({
                        [STATE_isIfElse]: false
                    });
                /** else가 존재하지 않는 경우 -> else 생성*/
                } else {
                    var selectedBlock = thisBlock.getLastElifBlock() || thisBlock;
                    var newBlock = blockContainerThis.createBlock(BLOCK_CODELINE_TYPE.ELSE );
                    newBlock.renderSelectedBlockBorderColor();
        
                    selectedBlock.getHolderBlock().appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                    thisBlock.ifElseBlock = newBlock;
                    newBlock.setParentBlock(thisBlock);

                    blockContainerThis.calculateDepthFromRootBlockAndSetDepth();
                    blockContainerThis.reRenderBlockList();
                    blockContainerThis.renderBlockLineNumberInfoDom(true);
                    thisBlock.setState({
                        [STATE_isIfElse]: true
                    });
                }
            });
        }

        if (blockCodeLineType == BLOCK_CODELINE_TYPE.FOR) {
            var containerButton = $(`<div class='${VP_CLASS_STYLE_FLEX_ROW_END}
                                                 vp-apiblock-elif-else-container-button' 
                                            style='width:160px; right:0; position:absolute; margin-top: -36px;'>
                                      </div>`);
         
            var toggleElseButton = $(`<div class='vp-apiblock-toggle-else-button'> else ${elseOnOffStr} </div>`);
            containerButton.append(toggleElseButton);
            $(blockMainDom).append(containerButton);
            $(toggleElseButton).click(function() {
                /** else가 존재하는 경우 -> else 삭제*/
                if (thisBlock.getState(STATE_isIfElse) == true) {
                    var elseBlock = thisBlock.ifElseBlock;
                    elseBlock.deleteLowerDepthChildBlocks();
                    thisBlock.ifElseBlock = null;
                    blockContainerThis.reRenderBlockList();
                    blockContainerThis.renderBlockLineNumberInfoDom(true);

                    thisBlock.setState({
                        [STATE_isIfElse]: false
                    });
                /** else가 존재하지 않는 경우 -> else 생성*/
                } else {
                    var selectedBlock = thisBlock.getLastElifBlock() || thisBlock;
                    var newBlock = blockContainerThis.createBlock(BLOCK_CODELINE_TYPE.FOR_ELSE );
                    newBlock.renderSelectedBlockBorderColor();
        
                    selectedBlock.getHolderBlock().appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                    thisBlock.ifElseBlock = newBlock;
                    newBlock.setParentBlock(thisBlock);

                    blockContainerThis.calculateDepthFromRootBlockAndSetDepth();
                    blockContainerThis.reRenderBlockList();
                    blockContainerThis.renderBlockLineNumberInfoDom(true);
                    thisBlock.setState({
                        [STATE_isIfElse]: true
                    });
                }
            });
        }

        if (blockCodeLineType == BLOCK_CODELINE_TYPE.TRY) {
            var finallyOnOffStr = STR_NULL;
            if (thisBlock.getState(STATE_isFinally) == true) {
                finallyOnOffStr = 'off';
            } else {
                finallyOnOffStr = 'on';
            }
            var containerButton = $(`<div class='${VP_CLASS_STYLE_FLEX_ROW_BETWEEN}
                                                  vp-apiblock-elif-else-container-button' 
                                          style='width:200px; right:0; position:absolute; margin-top: -36px;'>
                                        </div>`);
            var plusElifButton = $(`<div class='vp-apiblock-plus-elif-button'> + except </div>'`);
            var toggleElseButton = $(`<div class='vp-apiblock-toggle-else-button'> else ${elseOnOffStr} </div>`);
            var finallyButton = $(`<div class='vp-apiblock-toggle-else-button'> finally ${finallyOnOffStr} </div>`);

            containerButton.append(plusElifButton);
            containerButton.append(toggleElseButton);
            containerButton.append(finallyButton);

            $(blockMainDom).append(containerButton);
            $(plusElifButton).click(function(plusElifEvent) {
                var selectedBlock = thisBlock.getLastElifBlock() || thisBlock;
                var newBlock = blockContainerThis.createBlock(BLOCK_CODELINE_TYPE.EXCEPT);
                thisBlock.setLastElifBlock(newBlock);

                selectedBlock.getHolderBlock().appendBlock(newBlock, BLOCK_DIRECTION.DOWN);

                var elifConditionCode = GenerateIfConditionList(newBlock, BLOCK_CODELINE_TYPE.EXCEPT);
                $(`.vp-block-header-${newBlock.getUUID()}`).html(elifConditionCode);
               
                blockContainerThis.reRenderBlockList();
                blockContainerThis.renderBlockLineNumberInfoDom(true);
                blockContainerThis.calculateDepthFromRootBlockAndSetDepth();
    
                newBlock.renderSelectedBlockBorderColor();
                plusElifEvent.stopPropagation();
            });
            $(toggleElseButton).click(function() {
                /** else가 존재하는 경우 -> else 삭제*/
                if (thisBlock.getState(STATE_isIfElse) == true) {
                    var elseBlock = thisBlock.ifElseBlock;
                    elseBlock.deleteLowerDepthChildBlocks();
                    thisBlock.ifElseBlock = null;
                    blockContainerThis.reRenderBlockList();
                    blockContainerThis.renderBlockLineNumberInfoDom(true);

                    thisBlock.setState({
                        [STATE_isIfElse]: false
                    });
                /** else가 존재하지 않는 경우 -> else 생성*/
                } else {
                    var selectedBlock = thisBlock.getLastElifBlock() || thisBlock;
                    var newBlock = blockContainerThis.createBlock(BLOCK_CODELINE_TYPE.ELSE );
                    newBlock.renderSelectedBlockBorderColor();
        
                    selectedBlock.getHolderBlock().appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                    thisBlock.ifElseBlock = newBlock;
                    newBlock.setParentBlock(thisBlock);

                    blockContainerThis.calculateDepthFromRootBlockAndSetDepth();
                    blockContainerThis.reRenderBlockList();
                    blockContainerThis.renderBlockLineNumberInfoDom(true);
                    thisBlock.setState({
                        [STATE_isIfElse]: true
                    });
                }
            });

            $(finallyButton).click(function() {
                /** finally가 존재하는 경우 -> finally 삭제 */

                if (thisBlock.getState(STATE_isFinally) == true) {
                    var finallyBlock = thisBlock.finallyBlock;
                    finallyBlock.deleteLowerDepthChildBlocks();
                    thisBlock.finallyBlock = null;
                    blockContainerThis.reRenderBlockList();
                    blockContainerThis.renderBlockLineNumberInfoDom(true);

                    thisBlock.setState({
                        [STATE_isFinally]: false
                    });
                /** finally가 존재하지 않는 경우 -> finally 생성*/
                } else {
                    var selectedBlock;
                    if (thisBlock.ifElseBlock) {
                        selectedBlock = thisBlock.ifElseBlock;
                    } else {
                        selectedBlock = thisBlock.getLastElifBlock() || thisBlock;
                    }
                    var newBlock = blockContainerThis.createBlock(BLOCK_CODELINE_TYPE.FINALLY );
                    newBlock.renderSelectedBlockBorderColor();
        
                    selectedBlock.getHolderBlock().appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                    thisBlock.finallyBlock = newBlock;
                    newBlock.setParentBlock(thisBlock);

                    blockContainerThis.calculateDepthFromRootBlockAndSetDepth();
                    blockContainerThis.reRenderBlockList();
                    blockContainerThis.renderBlockLineNumberInfoDom(true);
                    thisBlock.setState({
                        [STATE_isFinally]: true
                    });
                }
            });
        }

        if (blockCodeLineType == BLOCK_CODELINE_TYPE.BLANK) {
            return;
        }       

        $(blockMainDom).append(deleteBtn);

        /** Block 삭제 버튼 클릭 */
        $(deleteBtn).click(function(event) { 
            thisBlock.deleteBlockFromDeleteBtn();

            blockContainerThis.setSelectedBlock(thisBlock);
            blockContainerThis.setIsOptionPageOpen(false);
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_DISPLAY, STR_NONE);
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_WIDTH, 0);
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MENU_BTN)).css(STR_RIGHT, 5);
         
        });

        if (blockCodeLineType == BLOCK_CODELINE_TYPE.BLANK
            || blockCodeLineType == BLOCK_CODELINE_TYPE.TRY 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.FINALLY
            || blockCodeLineType == BLOCK_CODELINE_TYPE.ELSE
            || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR_ELSE) {
                blockContainerThis.setSelectedBlock(thisBlock);
                blockContainerThis.setIsOptionPageOpen(false);
                $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_DISPLAY, STR_NONE);
                $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_WIDTH, 0);
                $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MENU_BTN)).css(STR_RIGHT, 5);
        } else {
            thisBlock.resetOptionPage();
            /** 옵션 페이지 다시 오픈 */
            blockContainerThis.setSelectedBlock(thisBlock);
            blockContainerThis.renderBlockOptionTab();
            thisBlock.renderOptionPage();
        }
    }
    /**
     * TODO: 추후 개선해야 할 메소드 
     * @async
     * block click시 발생하는 이벤트 메소드 
     */
    Block.prototype.bindClickEvent = function() {

        var thisBlock = this;
        var blockContainerThis = thisBlock.getBlockContainerThis();
        var blockMainDom = thisBlock.getBlockMainDom();

        /** block 클릭 */
        $(blockMainDom).click(async function(event){
            var blockCodeLineType = thisBlock.getBlockCodeLineType();
            blockContainerThis.bindCodeBlockInputFocus(thisBlock, blockCodeLineType);

            thisBlock.setIsClicked(true);
   
            if (event.ctrlKey == true){
                if (thisBlock.getIsCtrlPressed() == true) {
                    thisBlock.setIsCtrlPressed(false);
                }
            }

            /** 
             *  Block border color 리셋
             *  Block left holder의 font weight 300으로 변경
             */ 
            var blockList = blockContainerThis.getBlockList();
    
            for await (var block of blockList) {
                block.renderFontWeight300();
                block.renderResetColor();
            }

            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_BLOCK_DELETE_BTN)).remove();
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_BLOCK_OPTION_BTN)).remove();
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + 'vp-apiblock-elif-else-container-button')).remove();

            thisBlock.createSubButton();

            thisBlock.renderSelectedMainBlockBorderColor();

            /** 자식 하위 Depth Block Border 색칠 */
            thisBlock.renderSelectedBlockBorderColor();

        
            var childLowerDepthBlockList = thisBlock.getChildLowerDepthBlockList();
            childLowerDepthBlockList.forEach(block => {
                block.renderSelectedBlockBorderColor();
                block.renderFontWeight700();
            });

            thisBlock.setIsClicked(false);
            if (blockCodeLineType == BLOCK_CODELINE_TYPE.BLANK
                || blockCodeLineType == BLOCK_CODELINE_TYPE.TRY 
                || blockCodeLineType == BLOCK_CODELINE_TYPE.FINALLY
                || blockCodeLineType == BLOCK_CODELINE_TYPE.ELSE
                || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR_ELSE) {
                return;
            }

            blockContainerThis.setIsOptionPageOpen(true);
            var vpOptionPageRectWidth = blockContainerThis.getOptionPageWidth() || NUM_OPTION_PAGE_WIDTH;
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_DISPLAY, STR_BLOCK);
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_RIGHT, 0);
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_LEFT, 'initial');
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_WIDTH, vpOptionPageRectWidth);
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MENU_BTN)).css(STR_RIGHT, vpOptionPageRectWidth + 5);
        });
    }

    /** block을 x 버튼을 눌러 삭제할 때 실행되는 메소드 */
    Block.prototype.clickBlockDeleteButton = function() {
        var blockContainerThis = this.getBlockContainerThis();
        var blockCodeLineType = this.getBlockCodeLineType();
        this.deleteLowerDepthChildBlocks();
        this.resetOptionPage();
        
        /** else  for_else finally block 일 경우  */
        if (blockCodeLineType == BLOCK_CODELINE_TYPE.ELSE 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR_ELSE
            || blockCodeLineType == BLOCK_CODELINE_TYPE.FINALLY) {
            var parentBlock = this.getParentBlock()
            blockContainerThis.deleteElseBlockEvent(parentBlock, blockCodeLineType);
        }

        /** root block이 아니어야 block number 오름차순 sort 실행 */
        if (this.getPrevBlock() != null) {
            blockContainerThis.renderBlockLineNumberInfoDom(true);
        }

        blockContainerThis.reRenderBlockList();

        blockContainerThis.setSelectedBlock(this);
        blockContainerThis.setIsOptionPageOpen(false);
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_DISPLAY, STR_NONE);
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_WIDTH, 0);
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MENU_BTN)).css(STR_RIGHT, 5);
    }

    /** block shadow를 삭제하거나 만드는 메소드 2 */
    Block.prototype.renderBlockHolderShadow_2 = function(NONE_OR_BLOCK) {
        if ( this.getHolderBlock() ) {
            $( this.getHolderBlock().getBlockMainDom() ).css(STR_DISPLAY, NONE_OR_BLOCK);
        }
        var blockLeftHolderDom = this.getBlockLeftHolderDom();
        $(blockLeftHolderDom).css(STR_DISPLAY, NONE_OR_BLOCK);
    }


    /** Block Editor에 Scroll이 생성 될지 안 될지 결정하는 메소드
     *   0% ~70% 고정
     *   70% ~ 100% 상위로 이동 화면 scroll 조정 함
    */
    Block.prototype.renderEditorScrollTop = function(isNewBlock) {
        var blockContainerThis = this.getBlockContainerThis();
        var blockChildList = this.getRootBlock().getChildBlockList();
        
        var minusIndex = 0;
        var blockNumber = 0;

        blockChildList.some((block, index) => {
            if (block.getBlockCodeLineType() != BLOCK_CODELINE_TYPE.HOLDER) {
                if (this.getUUID() == block.getUUID()) {
                    blockNumber = index - minusIndex;
                    return true;
                }
            } else {
                minusIndex++;
            }
        });

        var maxHeight = blockContainerThis.getMaxHeight();
        var scrollHeight = blockContainerThis.getScrollHeight();

        if (scrollHeight >= maxHeight) {
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_SCROLLBAR)).css(STR_OVERFLOW_X, STR_HIDDEN);
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_SCROLLBAR)).css(STR_OVERFLOW_Y, STR_AUTO);

        } else {
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_SCROLLBAR)).css(STR_OVERFLOW_X, STR_HIDDEN);
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_SCROLLBAR)).css(STR_OVERFLOW_Y, STR_HIDDEN);
        }
        
        var eventClientY = blockContainerThis.getEventClientY();
        if (isNewBlock == true) {
         
        } else if (eventClientY < $(window).height() * 0.7) {
            return;
        }

        var thisBlockFromRootBlockHeight = 0;
        while(blockNumber != 0) {
            blockNumber--;
            thisBlockFromRootBlockHeight += NUM_BLOCK_MARGIN_TOP_PX;
            thisBlockFromRootBlockHeight += NUM_BLOCK_HEIGHT_PX;
            thisBlockFromRootBlockHeight += NUM_BLOCK_MARGIN_BOTTOM_PX;
        }

        if (thisBlockFromRootBlockHeight == 0) {
            thisBlockFromRootBlockHeight = blockContainerThis.getThisBlockFromRootBlockHeight();
             $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).animate({
                scrollTop: thisBlockFromRootBlockHeight 
            }, 100);
            return;
        } else {
            blockContainerThis.setThisBlockFromRootBlockHeight(thisBlockFromRootBlockHeight);  
        }
    
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).scrollTop(thisBlockFromRootBlockHeight);
    }

    Block.prototype.renderCodeLineDowned = function() {
        if ( this.getIsCodeLineDowned() == true ) {
            // var blockMainDom = this.getBlockMainDom();
            // $(blockMainDom).css(STR_MARGIN_TOP, 28);
        } else {
            // var blockMainDom = this.getBlockMainDom();
            // $(blockMainDom).css(STR_MARGIN_TOP, 0);
        }
    }

    /** this Block 부터 코드 실행 */
    Block.prototype.runThisBlock = function() {
        var thisBlock = this;
        var blockContainerThis = thisBlock.getBlockContainerThis();
        blockContainerThis.setIsBlockDoubleClicked(true);

        var code = STR_MSG_AUTO_GENERATED_BY_VISUALPYTHON + ' - ' +'API Block' + STR_KEYWORD_NEW_LINE;
        var childLowerDepthBlockList = thisBlock.getChildLowerDepthBlockList();
        var rootDepth = thisBlock.getDepth();
        childLowerDepthBlockList.forEach( ( block ) => {
            if ( block.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.HOLDER ) {
                return;
            }
            var depth = block.getDepth() - rootDepth;
          
            var indentPxStr = STR_NULL;
            var iteration = 0;
            while ( depth-- != 0) {
                indentPxStr += STR_ONE_INDENT;
                if (iteration > NUM_MAX_ITERATION) {
                    console.log(ERROR_AB0002_INFINITE_LOOP);
                    break;
                }
                iteration++;
            }

            code += indentPxStr + block.setCodeLineAndGet();
            code += STR_KEYWORD_NEW_LINE;
        });

        blockContainerThis.setAPIBlockCode(code);
        blockContainerThis.generateCode(true);
    }

    /** Block 오른쪽 x 버튼 혹은
     *  delete 키를 눌르면 block 삭제
     */
    Block.prototype.deleteBlockFromDeleteBtn = function() {
        var thisBlock = this;
        var blockContainerThis = thisBlock.getBlockContainerThis();
        var blockCodeLineType = thisBlock.getBlockCodeLineType();

        /** block에 ctrl + 클릭이 몇번 되었는지 체크 */
        var blockList = blockContainerThis.getBlockList();
        var numIsCtrlPressed = 0;
        var isCtrlPressedBlockList = [];
        blockList.some(block => {
            if ( block.getIsCtrlPressed() == true) {
                numIsCtrlPressed++;
                isCtrlPressedBlockList.push(block);
            };
        });
         
        /** block에 ctrl + 클릭이 2회 이상 */
        if ( numIsCtrlPressed > 1 ) {
            isCtrlPressedBlockList.some(block => {
                block.deleteLowerDepthChildBlocks();
                block.resetOptionPage();
                
                if ( blockCodeLineType == BLOCK_CODELINE_TYPE.ELSE 
                      || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR_ELSE
                      || blockCodeLineType == BLOCK_CODELINE_TYPE.FINALLY) {
                    var parentBlock = block.getParentBlock()
                    blockContainerThis.deleteElseBlockEvent(parentBlock, blockCodeLineType);
                }
         
                blockContainerThis.reRenderBlockList();
         
                /** root block이 아니어야 block number 오름차순 sort 실행 */
                if (block.getPrevBlock() != null) {
                    blockContainerThis.renderBlockLineNumberInfoDom(true);
                }
            });
         /** block에 ctrl + 클릭이 1회 이상 */
        } else {
            thisBlock.clickBlockDeleteButton(); 
        }
    }

    /**
     * Block Left Holder dom의 height 계산
     */
    Block.prototype._renderBlockLeftHolderListHeight = function() {
        var block = this;
        var leftHolderClientRect = $(block.getBlockLeftHolderDom())[0].getBoundingClientRect();
        var holderBlock = block.getHolderBlock();
        var holderBlockClientRect = $(holderBlock.getBlockMainDom())[0].getBoundingClientRect();
 
        var distance = holderBlockClientRect.y - leftHolderClientRect.y;

        $(block.getBlockLeftHolderDom()).css(STR_HEIGHT, distance);
        block.setTempBlockLeftHolderHeight(distance);
    }
 

    return {
        Block
    };
});
