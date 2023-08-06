define([
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/vpFuncJS'
    , 'nbextensions/visualpython/src/common/metaDataHandler'
    , 'nbextensions/visualpython/src/common/constant'

    , './api.js'
    , './config.js'
    , './constData.js'
    , './block.js'
    , './blockRenderer.js'
], function (vpCommon, vpFuncJS, md, vpConst,
             api, config, constData, block, blockRenderer ) {
    const { ChangeOldToNewState
            , UpdateOneArrayValueAndGet
            , DeleteOneArrayValueAndGet

            , DestructureFromBlockArray
            , RemoveSomeBlockAndGetBlockList

            , MakeFirstCharToUpperCase
            , FindStateValue
            , MapTypeToName
            , ControlToggleInput
        
            , IsCodeBlockType
            , IsCanHaveIndentBlock } = api;
    const { PROCESS_MODE } = config;
    const {  BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , BLOCK_DIRECTION
            , BLOCK_TYPE
            , MAKE_CHILD_BLOCK
            , FOCUSED_PAGE_TYPE

            , STR_CHANGE_KEYUP_PASTE
            , STR_COLON_SELECTED 

            , VP_CLASS_PREFIX 

            , VP_CLASS_BLOCK_NUM_INFO
            , VP_CLASS_BLOCK_CONTAINER

            , VP_CLASS_BLOCK_HEADER_PARAM
            , VP_CLASS_APIBLOCK_MAIN
            , VP_CLASS_APIBLOCK_BOARD
            , VP_CLASS_APIBLOCK_BUTTONS
            , VP_CLASS_APIBLOCK_OPTION_TAB
            , VP_CLASS_APIBLOCK_CODELINE_ELLIPSIS
            , VP_CLASS_APIBLOCK_INPUT_PARAM
            , VP_CLASS_APIBLOCK_PARAM_PLUS_BTN
            , VP_CLASS_APIBLOCK_PARAM_DELETE_BTN

            , NUM_INDENT_DEPTH_PX
            , NUM_MAX_ITERATION
            , NUM_DEFAULT_POS_Y
            , NUM_DEFAULT_POS_X
            , NUM_MAX_BLOCK_NUMBER
            , NUM_BLOCK_MAX_WIDTH
            , NUM_OPTION_PAGE_WIDTH
            , STR_NULL
            , STR_TOP
            , STR_LEFT
            , STR_DIV
            , STR_ONE_SPACE
            , STR_DOT
            , STR_SCROLLHEIGHT
            , STR_DATA_NUM_ID
            , STR_PX
            , STR_BORDER
            , STR_HEIGHT
            , STR_SPAN
            , STR_WIDTH
            , STR_MARGIN_LEFT
            , STR_MAX_WIDTH
            , STR_KEYWORD_NEW_LINE
            , STR_ONE_INDENT
            , STR_CLICK
            , STR_COLOR
            , STR_DATA_DEPTH_ID 

            , STR_BREAK
            , STR_CONTINUE
            , STR_PASS
            , STR_CODE
            , STR_PROPERTY
            , STR_OPACITY
            , STR_MSG_AUTO_GENERATED_BY_VISUALPYTHON

            , STATE_classInParamList
            , STATE_defInParamList
            , STATE_returnOutParamList

            , STATE_elifCodeLine
            , STATE_exceptCodeLine

            , STATE_breakCodeLine
            , STATE_continueCodeLine
            , STATE_passCodeLine
            , STATE_customCodeLine
            , STATE_propertyCodeLine
   

            , STATE_isIfElse
            , STATE_isForElse
            , STATE_isFinally

            , STATE_optionState

            , COLOR_CLASS_DEF
            , COLOR_CONTROL
            , COLOR_CODE
            , COLOR_FOCUSED_PAGE

            , API_BLOCK_PROCESS_DEVELOPMENT
        
            , ERROR_AB0002_INFINITE_LOOP } = constData;
 
    const { Block } = block;
    const { RenderFocusedPage
        
            , BindArrowBtnEvent} = blockRenderer;
         
            
    var BlockContainer = function() {
        this.importPackageThis = null;
        this.blockList = [];
        this.prevBlockList = [];
        this.nowMovedBlockList = [];
        this.blockHistoryStack = [];
        this.blockHistoryStackCursor = 0;

        this.resetBlockListButton = null;

        this.isDebugMode = false; 
        this.isBlockDoubleClicked = false;
        this.isMenubarOpen = false;
        this.isShowDepth = true;
        this.isOptionPageOpen = false;

        this.focusedPageType = FOCUSED_PAGE_TYPE;
        this.classNum = 1;
        this.defNum = 1;
        this.forNum = 1;
        this.thisBlockFromRootBlockHeight = 0;
        this.eventClientY = 0;
        this.optionPageWidth = NUM_OPTION_PAGE_WIDTH;
        this.selectedBlock = null;

        this.blockContainerDom = null;
        this.code = STR_NULL;

        this.mdHandler = null;  
        this.loadedVariableList = [];
    
    }

    BlockContainer.prototype.setMetahandler = function(funcID) {
        this.mdHandler = new md.MdHandler(funcID); 
    }

    BlockContainer.prototype.setImportPackageThis = function(importPackageThis) {
        this.importPackageThis = importPackageThis;
    }

    BlockContainer.prototype.getImportPackageThis = function() {
        return this.importPackageThis;
    }

    BlockContainer.prototype.setIsBlockDoubleClicked = function(isBlockDoubleClicked) {
        this.isBlockDoubleClicked = isBlockDoubleClicked;
    }

    BlockContainer.prototype.getIsBlockDoubleClicked = function() {
        return this.isBlockDoubleClicked;
    }

    BlockContainer.prototype.setIsMenubarOpen = function(isMenubarOpen) {
        this.isMenubarOpen = isMenubarOpen;
    }
    BlockContainer.prototype.getIsMenubarOpen = function() {
        return this.isMenubarOpen;
    }

    BlockContainer.prototype.setIsShowDepth = function(isShowDepth) {
        this.isShowDepth = isShowDepth;
    }
    BlockContainer.prototype.getIsShowDepth = function() {
        return this.isShowDepth;
    }

    BlockContainer.prototype.setIsOptionPageOpen = function(isOptionPageOpen) {
        this.isOptionPageOpen = isOptionPageOpen;
    }
    BlockContainer.prototype.getIsOptionPageOpen = function() {
        return this.isOptionPageOpen;
    }

    BlockContainer.prototype.setOptionPageWidth = function(optionPageWidth) {
        this.optionPageWidth = optionPageWidth;
    }
    BlockContainer.prototype.getOptionPageWidth = function() {
        return this.optionPageWidth;
    }


    /** Block 생성 */
    BlockContainer.prototype.createBlock = function(blockCodeLineType, isMetadata, blockData) {
        return new Block(this, blockCodeLineType, isMetadata, blockData);
    }

    /** block을 blockList에 add */
    BlockContainer.prototype.addBlock = function(block) {
        this.blockList = [...this.blockList, block];
    }

    /** blockList를 가져옴*/
    BlockContainer.prototype.getBlockList = function() {
        return this.blockList;
    }
    /** blockList를 파라미터로 받은 blockList로 덮어 씌움*/
    BlockContainer.prototype.setBlockList = function(blockList) {
        this.blockList = blockList;
    }

    /** prevBlockList를 가져옴*/
    BlockContainer.prototype.getPrevBlockList = function() {
        return this.prevBlockList;
    }
    /** prevBlockList를 파라미터로 받은 prevBlockList로 덮어 씌움*/
    BlockContainer.prototype.setPrevBlockList = function(prevBlockList) {
        this.prevBlockList = prevBlockList;
    }
    
    /** NowMovedBlockList를 가져옴*/
    BlockContainer.prototype.getNowMovedBlockList = function() {
        return this.nowMovedBlockList;
    }
    /** NowMovedBlockList를 파라미터로 받은 NowMovedBlockList로 덮어 씌움*/
    BlockContainer.prototype.setNowMovedBlockList = function(nowMovedBlockList) {
        this.nowMovedBlockList = nowMovedBlockList;
    }

    /** blockHistoryStack를 가져옴 */
    BlockContainer.prototype.getBlockHistoryStack = function() {
        return this.blockHistoryStack;
    }
    BlockContainer.prototype.getBlockLastHistoryStack = function() {
        return this.blockHistoryStack[this.blockHistoryStackCursor-1];
    }
    /** blockHistoryStack를 파라미터로 받은 blockHistoryStack로 덮어 씌움 */
    BlockContainer.prototype.setBlockHistoryStack = function(blockHistoryStack) {
        this.blockHistoryStack = blockHistoryStack;
    }

    /** blockHistoryStack에 최신 데이터를 push */
    BlockContainer.prototype.pushBlockHistoryStack = function(blockStack) {
        this.blockHistoryStack.push(blockStack);
        this.blockHistoryStackCursor += 1;
    }

    /** blockHistoryStack에 최신 데이터를 pop */
    BlockContainer.prototype.popBlockHistoryStackAndGet = function() {
        if (this.blockHistoryStackCursor < 0) {
            return;
        }
        this.blockHistoryStackCursor -= 1;
        // return this.blockHistoryStack.pop();
    }
    
    /** blockHistoryStack을 리셋합니다  */
    BlockContainer.prototype.resetStack = function() {
        this.blockHistoryStack = [];
    }

    /** root block을 get */
    BlockContainer.prototype.getRootBlock = function() {

        var blockList = this.getBlockList();
        var rootBlock = null;
        blockList.some(block => {
            if (block.getDirection() == BLOCK_DIRECTION.ROOT) {
                rootBlock = block;
                return true;
            }
        });
        return rootBlock;
    }

    /** ctrl + 클릭한 block들을 get */
    BlockContainer.prototype.getCtrlPressedBlockList = function() {
        var ctrlPressedBlockList = [];
        var blockList = this.getBlockList();
        blockList.forEach(block => {
            if ( block.getIsCtrlPressed() == true) {
                ctrlPressedBlockList.push(block);
            }
        });
        return ctrlPressedBlockList;
    }

    BlockContainer.prototype.setClassNum = function(classNum) {
        this.classNum = classNum;
    }
    BlockContainer.prototype.addClassNum = function() {
        this.classNum += 1;
    }
    BlockContainer.prototype.getClassNum = function() {
        return this.classNum;
    }

    BlockContainer.prototype.setDefNum = function(defNum) {
        this.defNum = defNum;
    }
    BlockContainer.prototype.addDefNum = function() {
        this.defNum += 1;
    }
    BlockContainer.prototype.getDefNum = function() {
        return this.defNum;
    }

    BlockContainer.prototype.setForNum = function(forNum) {
        this.forNum = forNum;
    }
    BlockContainer.prototype.addForNum = function() {
        this.forNum += 1;
    }
    BlockContainer.prototype.getForNum = function() {
        return this.forNum;
    }

    BlockContainer.prototype.getMaxWidth = function() {
        var maxWidth = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).width();
        return maxWidth;
    }

    BlockContainer.prototype.getMaxHeight = function() {
        var maxHeight = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).height();
        return maxHeight;
    }

    BlockContainer.prototype.getScrollHeight = function() {
        var scrollHeight = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).prop(STR_SCROLLHEIGHT);
        return scrollHeight;
    }

    BlockContainer.prototype.setThisBlockFromRootBlockHeight = function(thisBlockFromRootBlockHeight) {
        this.thisBlockFromRootBlockHeight = thisBlockFromRootBlockHeight;
    }
    BlockContainer.prototype.getThisBlockFromRootBlockHeight = function() {
        return this.thisBlockFromRootBlockHeight;
    }

    BlockContainer.prototype.setEventClientY = function(eventClientY) {
        this.eventClientY = eventClientY;
    }
    BlockContainer.prototype.getEventClientY = function() {
        return this.eventClientY;
    }

    BlockContainer.prototype.setResetBlockListButton = function(resetBlockListButton) {
        this.resetBlockListButton = resetBlockListButton;
    }
    BlockContainer.prototype.getResetBlockListButton = function() {
        return this.resetBlockListButton;
    }

    BlockContainer.prototype.setBlockContainerDom = function(blockContainerDom) {
        this.blockContainerDom = blockContainerDom;
    }
    BlockContainer.prototype.getBlockContainerDom = function() {
        return this.blockContainerDom;
    }

    BlockContainer.prototype.setSelectedBlock = function(selectedBlock) {
        this.selectedBlock = selectedBlock;
    }
    BlockContainer.prototype.getSelectedBlock = function() {
        return this.selectedBlock;
    }

    /** blockList에서 특정 block을 삭제
     * @param {string} blockUUID
     */
    BlockContainer.prototype.deleteBlock = function(blockUUID) {
        /** blockList를 돌며 삭제하고자 하는 block을 찾음.
         *  block은 고유의 UUID 
         *  파라미터로 들어온 block의 UUID가 blockList의 UUID와 일치하는 블럭이 있는지 찾는 과정.
         *  찾으면 isBlock true, blockList에서 index를 얻음
         *  못찾으면 isBlock false, 아무것도 하지 않고 메소드 작업을 종료.
         */
        var blockList = this.getBlockList();
        blockList.some((block, index) => {
            if (block.getUUID() == blockUUID) {
                delectedIndex = index;
                blockList.splice(index, 1);
                return true;
            } else {
                return false;
            }
        });
    }
    
    /** run 버튼 실행시 코드 실행 */
    BlockContainer.prototype.makeCode = function() {
        var rootBlock = this.getRootBlock();
        if (!rootBlock) {
            return;
        }
        var codeLineStrDataList = [];
        var codeLineStr = STR_NULL;
        // var currCodeLineLength = 0;

        var nextBlockList = rootBlock.getNextBlockList();
        var stack = [];

        if (nextBlockList.length !== 0) {
            stack.push(nextBlockList);
        }

        var travelBlockList = [rootBlock];

        var iteration = 0;
        var current;
        while (stack.length !== 0) {
            current = stack.shift();
            iteration++;
            if (iteration > NUM_MAX_ITERATION) {
                console.log(ERROR_AB0002_INFINITE_LOOP);
                break;
            }
            /** 배열 일 때 */
            if (Array.isArray(current)) {
                stack = DestructureFromBlockArray(stack, current);
            /** 배열이 아닐 때 */
            } else {
                var currBlock = current;
                if (currBlock.getBlockCodeLineType() !== BLOCK_CODELINE_TYPE.HOLDER) {
                    travelBlockList.push(currBlock);
                }
                var nextBlockList = current.getNextBlockList();
                stack.unshift(nextBlockList);
            }
        }

        travelBlockList.forEach( block => {
            var currBlock = block;
            var depth = currBlock.getDepth();
            var indentString = STR_NULL;
            while (depth-- !== 0) {
                indentString += STR_ONE_INDENT;
            }
            /** 각 Block의 blockCodeLine에 맞는 코드 생성 */
            var codeLine = currBlock.setCodeLineAndGet(indentString);

            /**  코드 라인 한 칸 띄우기 */    
            codeLine += STR_KEYWORD_NEW_LINE;
            codeLineStr += codeLine;
            currCodeLineLength = codeLineStr.length;
        });

        codeLineStrDataList.push({
            codeLineStr
        });
        var returnCodeLineStr = '';
        // var returnCodeLineStr = STR_MSG_AUTO_GENERATED_BY_VISUALPYTHON + ' - ' +'API Block' + STR_KEYWORD_NEW_LINE;
        codeLineStrDataList.forEach(codeLineStrData => {
            returnCodeLineStr += codeLineStrData.codeLineStr + STR_KEYWORD_NEW_LINE;
        });
        this.setAPIBlockCode(returnCodeLineStr);

        return returnCodeLineStr;
    }

    BlockContainer.prototype.makeAPIBlockMetadata = function() {
        var rootBlock = this.getRootBlock();
        if (!rootBlock) {
            return [];
        }

        var nextBlockList = rootBlock.getNextBlockList();
        var stack = [];

        if (nextBlockList.length !== 0) {
            stack.push(nextBlockList);
        }
        var travelBlockList = [rootBlock];

        var iteration = 0;
        var current;
        while (stack.length !== 0) {
            current = stack.shift();
            iteration++;
            if (iteration > NUM_MAX_ITERATION) {
                console.log(ERROR_AB0002_INFINITE_LOOP);
                break;
            }
            /** 배열 일 때 */
            if (Array.isArray(current)) {
                stack = DestructureFromBlockArray(stack, current);
            /** 배열이 아닐 때 */
            } else {
                var currBlock = current;
                travelBlockList.push(currBlock);
                var nextBlockList = current.getNextBlockList();
                stack.unshift(nextBlockList);
            }
        }

        var apiBlockJsonDataList = [];
        travelBlockList.forEach( (block, index) => {
            var nextBlockUUIDList = [ ...block.getNextBlockList().map(nextBlock => {
                    return nextBlock.getUUID();
                })
            ]
            apiBlockJsonDataList[index] = {
                UUID: block.getUUID()
                , prevBlockUUID: block.getPrevBlock() 
                                            ? block.getPrevBlock().getUUID() 
                                            : -1
                , nextBlockUUIDList
                , blockType: block.getBlockCodeLineType()
                , blockName: block.getBlockName()
                , blockOptionState: block.getState(STATE_optionState)
                , blockDepth: block.getDepth()
                , blockDirection: block.getDirection()
            }
        });
        return apiBlockJsonDataList;
    }

    BlockContainer.prototype.pushNowBlockList = function() {
        var apiBlockJsonDataList = this.makeAPIBlockMetadata();
        this.pushBlockHistoryStack(apiBlockJsonDataList);
    }

    BlockContainer.prototype.reRenderBlockList_fromMetadata = function(apiBlockJsonDataList) {
        var blockContainerThis = this;

        /** block container dom 생성 */
        var _containerDom = blockContainerThis.getBlockContainerDom();
        $(_containerDom).remove();

        var containerDom = document.createElement(STR_DIV);
        containerDom.classList.add(VP_CLASS_BLOCK_CONTAINER);
        blockContainerThis.setBlockContainerDom(containerDom);

        $(containerDom).css(STR_TOP,`${NUM_DEFAULT_POS_Y}${STR_PX}`);
        $(containerDom).css(STR_LEFT,`${NUM_DEFAULT_POS_X}${STR_PX}`);

        /** metadata json을 기반으로 블럭 렌더링 */
        var createdBlockList = [];
        var createdBlock = null;
        apiBlockJsonDataList.forEach( (blockData, index) => {
            const { UUID, prevBlockUUID, nextBlockUUIDList
                     , blockType, blockName, blockOptionState, blockDepth, blockDirection } = blockData;
            createdBlock = blockContainerThis.createBlock(blockType, blockData);
            createdBlock.setUUID(UUID);
            createdBlock.setDepth(blockDepth);
            createdBlock.setDirection(blockDirection);
            createdBlock.setBlockName(blockName);
            createdBlock.setState({
                optionState: blockOptionState
            });
            createdBlock.setNextBlockUUIDList(nextBlockUUIDList);
            createdBlockList.push(createdBlock);
        });

        var _nextBlockUUIDList = [];
        var i = 0;
        createdBlockList.forEach((createdBlock,index) => {
            _nextBlockUUIDList = createdBlock.getNextBlockUUIDList();
            _nextBlockUUIDList.forEach(uuid => {

                createdBlockList.forEach(nextCreatedBlock => {
                    if (uuid == nextCreatedBlock.getUUID()) {
                        i++;
                        nextCreatedBlock.setPrevBlock(createdBlock);
                        createdBlock.addNextBlockList(nextCreatedBlock);
                        if (IsCanHaveIndentBlock(createdBlock.getBlockCodeLineType()) 
                            && nextCreatedBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.HOLDER) {
                            createdBlock.setHolderBlock(nextCreatedBlock);
                        }
                    }           
                });
            });
        });

        this.setBlockList(createdBlockList);

        this.calculateDepthFromRootBlockAndSetDepth();
        this.reRenderBlockList(true);
        this.renderBlockLineNumberInfoDom(true);

    }


    BlockContainer.prototype.getAPIBlockCode = function() {
        return this.code;
    }
    BlockContainer.prototype.setAPIBlockCode = function(code) {
        this.code = code;
    }
    
    BlockContainer.prototype.setFocusedPageType = function(focusedPageType) {
        this.focusedPageType = focusedPageType;
    }
    BlockContainer.prototype.getFocusedPageType = function() {
        return this.focusedPageType;
    }
    BlockContainer.prototype.setFocusedPageTypeAndRender = function(focusedPageType) {
        this.setFocusedPageType(focusedPageType);
        RenderFocusedPage(focusedPageType);
    }

    /** */
    BlockContainer.prototype.renderChildBlockListIndentAndGet = function() {

        var rootDepth = 0;
        var rootBlock = this.getRootBlock();
        if (rootBlock == null) {
            return [];
        }
        rootBlock.setDepth(rootDepth);

        //** root Block의 자식 Block depth */
        var childBlockList = rootBlock.getChildBlockList();
        childBlockList.forEach(async (block, index) => {

            var depth = block.calculateDepthAndGet();
            block.setDepth(depth);

            /** index 0일때 rootDepth를 계산*/
            if (index == 0) {
                rootDepth = depth;
                return;
            }
            /** index 1 이상 일때 */
            var indentPxNum = 0;
            while (depth-- != 0) {
                indentPxNum += NUM_INDENT_DEPTH_PX;
            }
        
            var numWidth = NUM_BLOCK_MAX_WIDTH - indentPxNum;
            var blockMainDom = block.getBlockMainDom();
      
            $(blockMainDom).css(STR_MARGIN_LEFT, indentPxNum + STR_PX);
            $(blockMainDom).css(STR_WIDTH, numWidth);
        });
        return childBlockList;
    }

    /** 
     * @async
     * Block editor에 존재하는 블럭들을 전부 다시 렌더링한다 
     */
    BlockContainer.prototype.reRenderBlockList = async function(isMetaData) {
       // console.log('----------------------reRenderBlockList----------------------');
       var prevBlockList = this.getPrevBlockList();
    //    console.log('prevBlockList',prevBlockList);
       var blockList = this.renderChildBlockListIndentAndGet();
    //    console.log('blockList',blockList);
       if (isMetaData == true) {
       
            {
                var _containerDom = this.getBlockContainerDom();
                $(_containerDom).empty();
                $(_containerDom).remove();
                $("." + VP_CLASS_BLOCK_CONTAINER).remove();
            }
    
            var newContainerDom = document.createElement(STR_DIV);
            newContainerDom.classList.add(VP_CLASS_BLOCK_CONTAINER);
            this.setBlockContainerDom(newContainerDom);

            // var newContainerDom = this.getBlockContainerDom();
            $(newContainerDom).css(STR_TOP, `${NUM_DEFAULT_POS_Y}` + STR_PX);
            $(newContainerDom).css(STR_LEFT, `${NUM_DEFAULT_POS_X}` + STR_PX);

            for await (var block of blockList) {
                new Promise( (resolve) => resolve( $(newContainerDom).append(block.getBlockMainDom())));
                block.bindEventAll();
            }
            this.setPrevBlockList(blockList);
            $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD).append(newContainerDom);
            return;
       } else if ( blockList < prevBlockList ) {
            // console.log(' blockList < prevBlockList');
            var deletedBlockList = RemoveSomeBlockAndGetBlockList(prevBlockList, blockList);
            deletedBlockList.forEach(block => {
               var blockMainDom = block.getBlockMainDom();
               $(blockMainDom).remove();
            });

            this.setPrevBlockList(blockList);
         
            return;
       } else if (blockList > prevBlockList) {
            // console.log(' blockList > prevBlockList');
            var containerDom = this.getBlockContainerDom();
            var addedBlockList = RemoveSomeBlockAndGetBlockList(blockList, prevBlockList);
            var prevBlock = addedBlockList[0].getPrevBlock();
            if (prevBlock === null) {
               addedBlockList.forEach((addedBlock,index) => {
                   $(containerDom).append(addedBlock.getBlockMainDom() );
           
                   addedBlock.bindEventAll();
               });
           } else {
               addedBlockList.forEach(addedBlock => {
                   $( addedBlock.getBlockMainDom() ).insertAfter(prevBlock.getBlockMainDom());
       
                   addedBlock.bindEventAll();
                   prevBlock = addedBlock;
               });
           }
           this.setPrevBlockList(blockList);

           return;
       } else {
            // console.log('여기4');

           {
               var _containerDom = this.getBlockContainerDom();
               $(_containerDom).empty();
               $(_containerDom).remove();
               $("." + VP_CLASS_BLOCK_CONTAINER).remove();
           }
    
           var containerDom = document.createElement(STR_DIV);
           containerDom.classList.add(VP_CLASS_BLOCK_CONTAINER);
           this.setBlockContainerDom(containerDom);

           $(containerDom).css(STR_TOP, `${NUM_DEFAULT_POS_Y}` + STR_PX);
           $(containerDom).css(STR_LEFT, `${NUM_DEFAULT_POS_X}` + STR_PX);
   
           for await (var block of blockList) {
              new Promise( (resolve) => resolve( $(containerDom).append(block.getBlockMainDom())));
              block.bindEventAll();
           }
           this.setPrevBlockList(blockList);
       }
        $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD).append(containerDom);

    }

     /** Block 앞에 line number를 정렬
      * isAsc true면 오름차순 정렬
     */
     BlockContainer.prototype.renderBlockLineNumberInfoDom = async function(isAsc) {

        var rootBlock = this.getRootBlock();
        if (!rootBlock) {
            return;
        }

        var blockChildList = rootBlock.getChildBlockList();
        var minusIndex = 0;

        var blockAmount = 0;
        blockChildList.forEach((block, index) => {
            if (block.getBlockCodeLineType() !== BLOCK_CODELINE_TYPE.HOLDER) {
                blockAmount++;
            }
        });

        blockChildList.forEach(async (block,index) => {
            var index = index + 1;
            if (block.getBlockCodeLineType() !== BLOCK_CODELINE_TYPE.HOLDER) {
                var blockDepth = block.getDepth();
                var numberPx = -(NUM_INDENT_DEPTH_PX * blockDepth + NUM_DEFAULT_POS_X - 3);

                var $blockLineNumberInfoDom = $(block.getBlockLineNumberInfoDom());
                $blockLineNumberInfoDom.css( STR_LEFT, numberPx + STR_PX );

                var blockLineNumber = 0;
                /** Line number 오름차순 정렬의 경우 */
                if (isAsc == true) {
                    $blockLineNumberInfoDom.css(STR_COLOR, '#828282');
                    block.setIsMoved(false);
                    blockLineNumber = index - minusIndex;
                /** 처음 생성한 Line number를 그대로 보여줄 경우 */
                } else {
                    if ( block.getIsMoved() == true ) {
                        $blockLineNumberInfoDom .css(STR_COLOR, COLOR_FOCUSED_PAGE);
                    }
                    blockLineNumber = block.getBlockNumber();
                    block.setBlockNumber(blockLineNumber);
                }

                block.setBlockNumber(blockLineNumber);
                if (blockLineNumber >= NUM_MAX_BLOCK_NUMBER) {
                    blockLineNumber = NUM_MAX_BLOCK_NUMBER;
                }

                var prefixNumInfo = this.makeBlockLineNumberstr( blockAmount, blockLineNumber );
                $blockLineNumberInfoDom.find('.vp-block-prefixnum-info').text(prefixNumInfo);
                $blockLineNumberInfoDom.find('.vp-block-linenumber-info').text(blockLineNumber);

                if (block.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.BLANK) {
                    $(block.getBlockMainDom()).find('.vp-block-depth-info').css(STR_OPACITY,0);
                } 
          
            } else {
                /** 그림자 블럭(holder block)이 나오면 다음번 블럭의 index 계산 할때,
                 *  지금 까지 그림자 블럭(holder block) 나온 횟수 만큼 감소 
                 */
                minusIndex++;
            }
        });
    }
    
    /** line number 앞에 prefix로 0 붙여주는 메소드 */
    BlockContainer.prototype.makeBlockLineNumberstr = function(blockAmount, blockLineNumber) {
        var prefixNuminfo = '';
        if ( blockAmount >= 1000 ) {
            if ( blockLineNumber >= 1000 ){
    
            } else if ( blockLineNumber >= 100 ) {
                prefixNuminfo += '0';
            } else if ( blockLineNumber >= 10 ) {
                prefixNuminfo += '00';
            } else {
                prefixNuminfo += '000';
            }
        } else if ( blockAmount >= 100 ) {
            if ( blockLineNumber >= 1000 ){
    
            } else if ( blockLineNumber >= 100 ) {
          
            } else if ( blockLineNumber >= 10 ) {
           
                prefixNuminfo += '0';
            } else {
            
                prefixNuminfo += '00';
            }
        } else if ( blockAmount >= 10) {
            if ( blockLineNumber >= 10) {
    
            } else {
                prefixNuminfo += `0`;
            }
           
        } else {
    
        }
        return prefixNuminfo;
    }

    /**
     * @param {BLOCK} checkBlock 
     */
    BlockContainer.prototype.getRootToLastBottomBlock = function() {
        var rootBlock = this.getRootBlock();
        // console.log('rootBlock', rootBlock);
        return this.getLastBottomBlock(rootBlock);
    }

    /**
     * @param {BLOCK} thatBlock 
     * @param {BLOCK} checkBlock 
     */
    BlockContainer.prototype.getLastBottomBlock = function(thatBlock) {
        var nextBlockList = thatBlock.getNextBlockList();
        var stack = [];
        if (nextBlockList.length !== 0) {
            stack.push(nextBlockList);
        }

        var current = null;
        while (stack.length !== 0) {
            current = stack.shift();
            if (Array.isArray(current)) {
                current.forEach(block => {
                    if (block.getDirection() == BLOCK_DIRECTION.DOWN) {
                        stack.unshift(block);
                    }
                });
            } else{
                var nextBlockList = current.getNextBlockList();
                var isDownBlock = nextBlockList.some(nextBlock => {
                    if (nextBlock.getDirection() == BLOCK_DIRECTION.DOWN) {
                        current = nextBlock;
                        stack.unshift(nextBlock);
                        return true;
                    }
                });
                if ( !isDownBlock ) {
                    break;
                }
            }
        }
        return current;
    }

    /** else block을 생성, 삭제하는 함수를 bind하는 이벤트 함수  
     * @param {if or for or try BLOCK} thatBlock 
     * @param {ELSE or FOR_ELSE or FINALLY} blockCodeLineType 
     */
    BlockContainer.prototype.bindElseBlockEvent = function(thatBlock, blockCodeLineType) {
        var blockContainerThis = this;
        var stateStr = '';
        var name = '';
        if (blockCodeLineType == BLOCK_CODELINE_TYPE.ELSE) {
            stateStr = STATE_isIfElse;
            name = 'else';
        } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.FOR_ELSE) {
            stateStr = STATE_isForElse;
            name = 'else';
        } else {
            stateStr = STATE_isFinally;
            name = 'finally';
        }
        var uuid = thatBlock.getUUID();

        /** else yes */
        $(document).off(STR_CLICK, `.vp-apiblock-${name}-yes-${uuid}`);
        $(document).on(STR_CLICK, `.vp-apiblock-${name}-yes-${uuid}`, function() {
            if (thatBlock.getState(stateStr) == true) {
                blockContainerThis.renderBlockOptionTab();
                return;
            }

            thatBlock.setState({
                [`${stateStr}`]: true
            });
        
            var selectedBlock = thatBlock.getLastElifBlock() || thatBlock;
            var newBlock = blockContainerThis.createBlock(blockCodeLineType );
            newBlock.renderSelectedBlockBorderColor();

            selectedBlock.getHolderBlock().appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
            if (blockCodeLineType == BLOCK_CODELINE_TYPE.ELSE) {
                thatBlock.ifElseBlock = newBlock;
            } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.FOR_ELSE) {
                thatBlock.forElseBlock = newBlock;
                thatBlock.setForElseBlock(newBlock);
            } else {
                thatBlock.finallyBlock = newBlock;
            }

            newBlock.setParentBlock(thatBlock);

            blockContainerThis.calculateDepthFromRootBlockAndSetDepth();
            blockContainerThis.renderBlockOptionTab();   
 
            $(`.vp-apiblock-${name}-yes-${uuid}`).css(STR_BORDER, `2px solid yellow`);
            $(`.vp-apiblock-${name}-no-${uuid}`).css(STR_BORDER, `2px solid #E85401`);

            blockContainerThis.reRenderBlockList();
            blockContainerThis.renderBlockLineNumberInfoDom(true);
        });

        /** else no */
        $(document).off(STR_CLICK, `.vp-apiblock-${name}-no-${uuid}`);
        $(document).on(STR_CLICK, `.vp-apiblock-${name}-no-${uuid}`, function() {
            blockContainerThis.deleteElseBlockEvent(thatBlock, blockCodeLineType);
        });
    }

    /** else block을 삭제하는 메소드 */
    BlockContainer.prototype.deleteElseBlockEvent = function(thatBlock, blockCodeLineType) {
        var blockContainerThis = this
        var uuid = thatBlock.getUUID();

        var stateStr = '';
        var name = '';
        if (blockCodeLineType == BLOCK_CODELINE_TYPE.ELSE) {
            stateStr = STATE_isIfElse;
            name = 'else';
        } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.FOR_ELSE) {
            stateStr = STATE_isForElse;
            name = 'else';
        } else {
            stateStr = STATE_isFinally;
            name = 'finally';
        }

        if (thatBlock.getState(stateStr) == false) {  
            blockContainerThis.renderBlockOptionTab();   
            return;
        }

        thatBlock.setState({
            [`${stateStr}`]: false
        });

        var elseBlock;
        if (blockCodeLineType == BLOCK_CODELINE_TYPE.ELSE) {
            elseBlock = thatBlock.ifElseBlock;
        } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.FOR_ELSE) {
            elseBlock = thatBlock.forElseBlock;
        } else {
            elseBlock = thatBlock.finallyBlock;
        }
        elseBlock.deleteLowerDepthChildBlocks();

        if (blockCodeLineType == BLOCK_CODELINE_TYPE.ELSE) {
            thatBlock.ifElseBlock = null;
        } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.FOR_ELSE) {
            thatBlock.forElseBlock = null;
        } else {
            thatBlock.finallyBlock = null;
        }

        $(`.vp-apiblock-${name}-no-${uuid}`).css(STR_BORDER, `2px solid yellow`);
        $(`.vp-apiblock-${name}-yes-${uuid}`).css(STR_BORDER, `2px solid #E85401`);

        blockContainerThis.reRenderBlockList();
        blockContainerThis.renderBlockLineNumberInfoDom(true);
        blockContainerThis.renderBlockOptionTab();   
    }

    /** Code block을 생성하면 옵션 페이지의 input 태그에 focus 하는 메소드 
     * @param { Block } block
     * @param { enum } blockCodeLineType
     */
    BlockContainer.prototype.bindCodeBlockInputFocus = function(block) {
        var uuid = block.getUUID();
        var blockCodeLineType = block.getBlockCodeLineType();
        if ( IsCodeBlockType(blockCodeLineType) ) {
                
            ControlToggleInput();
            var goFocus = function() {
                $(`#vp_apiblockCodeOptionInput${uuid}`).focus(); 
              
                /** 처음 한 번 실행하고 사라지는 특수한 이벤트 함수 */
                $(document).off(STR_CHANGE_KEYUP_PASTE, `#vp_apiblockCodeOptionInput${uuid}`);
                $(document).on(STR_CHANGE_KEYUP_PASTE, `#vp_apiblockCodeOptionInput${uuid}`, function(event) {
                    var inputValue = $(this).val();
                    var slicedInputValue_before = STR_NULL;

                    if ( blockCodeLineType == BLOCK_CODELINE_TYPE.CODE 
                        ||blockCodeLineType == BLOCK_CODELINE_TYPE.COMMENT
                        ||blockCodeLineType == BLOCK_CODELINE_TYPE.PRINT ) {
                        $(`#vp_apiblockCodeOptionInput${uuid}`).focus(); 
                    } else{
                        var index = -1;
                        /** PASS 블럭 */
                        if ( blockCodeLineType == BLOCK_CODELINE_TYPE.PASS ) {
                            index = inputValue.indexOf(STR_PASS);
                        /** PROPERTY 블럭 */
                        } else if ( blockCodeLineType == BLOCK_CODELINE_TYPE.PROPERTY ) {
                            index = inputValue.indexOf(STR_PROPERTY);
                        /** BREAK 블럭 */
                        } else if ( blockCodeLineType == BLOCK_CODELINE_TYPE.BREAK ) {
                            index = inputValue.indexOf(STR_BREAK);
                         /** Continue 블럭 */
                        } else {
                            index = inputValue.indexOf(STR_CONTINUE);
                        }

                        if ( index != -1) {
                            slicedInputValue_before = inputValue.slice(0, index);
                            block.setState({
                                customCodeLine: slicedInputValue_before
                            });
                            $(`#vp_apiblockCodeOptionInput${uuid}`).val(slicedInputValue_before);
                            $(`.vp-block-header-${uuid}`).html(slicedInputValue_before);
                        } else {
                            $(`#vp_apiblockCodeOptionInput${uuid}`).focus(); 
                        }
                    } 
   
                    event.stopPropagation();
                });
            } 
            var goInfinite = function() { 
                setTimeout(function(){ 
                    goFocus(); 
                },0);
            }
            goInfinite();
        }
    }

    /**
     *  옵션 페이지의 child Options 를 렌더링하는 메소드
     */
    BlockContainer.prototype.renderBlockOptionTab = function() {
        var selectedBlock = this.getSelectedBlock();
        if(selectedBlock) {
            selectedBlock.resetOptionPage();
            selectedBlock.renderOptionPage();
            BindArrowBtnEvent();
        }
    }

    /** importPackage의 generateCode 이전에 실행할 prefix code
     *  @param {boolean} isClicked true면 클릭 이벤트로 코드 실행
     */
    BlockContainer.prototype.generateCode = function(isClicked) {
        var importPackageThis = this.getImportPackageThis();
        importPackageThis.generateCode(true, true, isClicked);
    }


    /**
     * block의 depth를 계산하고 block 앞에 depth 를 보여주는 함수
     */
    BlockContainer.prototype.calculateDepthFromRootBlockAndSetDepth = function() {
        var rootBlock = this.getRootBlock();
        if (!rootBlock) {
            return;
        }
        var getChildBlockList = rootBlock.getChildBlockList();

        getChildBlockList.forEach((block) => {
            if (block.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.HOLDER) {
                return;
            }
            var depth = block.calculateDepthAndGet();
            var blockDepthInfoDom = block.getBlockDepthInfoDom();
            blockDepthInfoDom.text(depth);
        });
    }



    /**  LoadedVariableList  예제
    0:
    varName: "cam"
    varType: "DataFrame"
    1:
    varName: "lol"
    varType: "DataFrame"
    2:
    varName: "wea"
    varType: "DataFrame"
    3:
    varName: "wel2"
    varType: "DataFrame"
    */

    BlockContainer.prototype.setKernelLoadedVariableList = function(loadedVariableList) {
        this.loadedVariableList = loadedVariableList;
    }

    /** varName varType를 Array로 다 가져오기*/
    BlockContainer.prototype.getKernelLoadedVariableList = function() {
        return this.loadedVariableList;
    }

    /** varName만 Array로 가져오기*/
    BlockContainer.prototype.getKernelLoadedVariableNameList = function() {
        return this.loadedVariableList.map(varData => {
            return varData.varName;
        });
    }
    /** metadata init */
    BlockContainer.prototype.setAPIBlockMetadataHandler = function() {  
        var importPackageThis = this.getImportPackageThis();
        this.setMetahandler(importPackageThis.funcID);
        this.mdHandler.generateMetadata(importPackageThis);  
        this.mdHandler.metadata.apiblockList = [];

        // importPackageThis.metadata = metadata;
    }

    /** metadata set */
    BlockContainer.prototype.setAPIBlockMetadata = function() {  
        var importPackageThis = this.getImportPackageThis();  
        var apiBlockJsonDataList = this.makeAPIBlockMetadata();  
        var encoded_apiBlockJsonDataList = encodeURIComponent(JSON.stringify(apiBlockJsonDataList));
        
        /** API BLOCK container가 가지고 있는 metadata 
         *  이 데이터는 API Block가 metadata를 핸들링하기 위해 존재
         */
        this.mdHandler.metadata.apiblockList = encoded_apiBlockJsonDataList;
        /** importPackage가 가지고 있는 metadata 
         *  이 데이터는 #vp_saveOn 버튼을 누를시 vpNote로 간다.
        */
        importPackageThis.metadata = this.mdHandler.metadata;        
    }

    /** metadata 로드 */
    BlockContainer.prototype.loadAPIBlockMetadata = function(loadedMetadata) {
        if (loadedMetadata) {
            var importPackageThis = this.getImportPackageThis(); 
            var decodedMetadata = decodeURIComponent(loadedMetadata.apiblockList);
            var parsedDecodedMetadata = JSON.parse(decodedMetadata);

            this.mdHandler.metadata = loadedMetadata;
            this.mdHandler.metadata.apiblockList = parsedDecodedMetadata;
            importPackageThis.metadata = this.mdHandler.metadata;  

            this.reRenderBlockList_fromMetadata(parsedDecodedMetadata);   
        } 
    }

    /** metadata 세이브 */
    BlockContainer.prototype.saveAPIBlockMetadata = function(isMessage = false) {  
        var apiBlockJsonDataList = this.makeAPIBlockMetadata();  

        var importPackageThis = this.getImportPackageThis();  

        var encoded_apiBlockJsonDataList = encodeURIComponent(JSON.stringify(apiBlockJsonDataList));
        this.mdHandler.metadata.apiblockList = encoded_apiBlockJsonDataList;

        importPackageThis.metadata = this.mdHandler.metadata;  

        this.mdHandler.saveMetadata(this.mdHandler.metadata);
        
    }

    return BlockContainer;
});
