define([
    'nbextensions/visualpython/src/common/vpCommon'

    , './api.js'
    , './constData.js'
    , './block.js'
    , './shadowBlock.js'
    , './blockRenderer.js'
], function (vpCommon, api, constData, blockData, shadowBlock, blockRenderer ) {
    const { ChangeOldToNewState
            , FindStateValue
            , MapTypeToName
            , pxStrToNum } = api;
    const { BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , BLOCK_DIRECTION
            , BLOCK_TYPE
            , MAKE_CHILD_BLOCK 
            , FOCUSED_PAGE_TYPE

            , NUM_BLOCK_HEIGHT_PX
            , NUM_INDENT_DEPTH_PX
            , NUM_MAX_ITERATION
            , NUM_ZERO
            , NUM_DEFAULT_POS_X
            , NUM_DEFAULT_POS_Y
            , NUM_BLOCK_MARGIN_TOP_PX
            , NUM_BLOCK_MARGIN_BOTTOM_PX
            , NUM_EXCEED_DEPTH

            , STR_TOP
            , STR_LEFT
            , STR_DIV
            , STR_BORDER
            , STR_PX
            , STR_OPACITY
            , STR_MARGIN_TOP
            , STR_MARGIN_LEFT
            , STR_DISPLAY
            , STR_BACKGROUND_COLOR
            , STR_HEIGHT
            , STR_YES
            , STR_DATA_NUM_ID 
            , STR_DATA_DEPTH_ID
            , STR_NONE
            , STR_BLOCK
            , STR_CLICK

            , VP_CLASS_PREFIX
            , VP_CLASS_APIBLOCK_MAIN    
            , VP_CLASS_APIBLOCK_OPTION_TAB
            , VP_CLASS_APIBLOCK_MENU_BTN
            , VP_CLASS_BLOCK_CONTAINER
            , VP_CLASS_BLOCK_SHADOWBLOCK
            , VP_CLASS_BLOCK_DELETE_BTN
            , VP_CLASS_BLOCK_SHADOWBLOCK_CONTAINER

            , VP_CLASS_APIBLOCK_BOARD

            , VP_CLASS_BLOCK_OPTION_BTN } = constData;  
    const {  } = blockData;
    const { RenderFocusedPage
            , RenderHTMLDomColor } = blockRenderer;
    const ShadowBlock = shadowBlock;

    var CreateBlockBtn = function(blockContainerThis, type) { 
        this.blockContainerThis = blockContainerThis;
        this.state = {
            type
            , name: ''
        }
        this.rootDomElement = null;

        this.setState({
            name: MapTypeToName(type)
        });
        this.render();
        this.bindBtnDragEvent();
    }

    CreateBlockBtn.prototype.getBlockContainerThis = function() {
        return this.blockContainerThis;
    }


    CreateBlockBtn.prototype.getBlockName = function() {
        return this.state.name;
    }

    CreateBlockBtn.prototype.setBlockName = function(name) {
        this.setState({
            name
        });
    }
    CreateBlockBtn.prototype.getBlockCodeLineType = function() {
        return this.state.type;
    }






    CreateBlockBtn.prototype.getBlockMainDom = function() {
        return this.rootDomElement;
    }

    CreateBlockBtn.prototype.setBlockMainDom = function(rootDomElement) {
        this.rootDomElement = rootDomElement;
    }
    CreateBlockBtn.prototype.getBlockMainDomPosition = function() {
        var rootDom = this.getBlockMainDom();
        var clientRect = $(rootDom)[0].getBoundingClientRect();
        return clientRect;
    }







    // ** Block state 관련 메소드들 */
    CreateBlockBtn.prototype.setState = function(newState) {
        this.state = ChangeOldToNewState(this.state, newState);
        this.consoleState();
    }
    /**
        특정 state Name 값을 가져오는 함수
        @param {string} stateKeyName
    */
    CreateBlockBtn.prototype.getState = function(stateKeyName) {
        return FindStateValue(this.state, stateKeyName);
    }
    CreateBlockBtn.prototype.getStateAll = function() {
        return this.state;
    }
    CreateBlockBtn.prototype.consoleState = function() {
        // console.log(this.state);
    }






    CreateBlockBtn.prototype.render = function() {
        var blockContainer = null;
        var rootDomElement = $(`<div class='vp-apiblock-tab-navigation-node-block-body-btn'>
                                    <span class='vp-block-name'>
                                        ${this.getBlockName()}
                                    </span>
                                </div>`);

        this.setBlockMainDom(rootDomElement);
        rootDomElement = RenderHTMLDomColor(this, rootDomElement);

        var blockCodeType = this.getBlockCodeLineType();
        if (blockCodeType == BLOCK_CODELINE_TYPE.CLASS 
            || blockCodeType == BLOCK_CODELINE_TYPE.DEF) {
            blockContainer = $(`.vp-apiblock-tab-navigation-node-subblock-1-body-inner`);
    
        } else if (blockCodeType == BLOCK_CODELINE_TYPE.IF 
            || blockCodeType == BLOCK_CODELINE_TYPE.FOR
            || blockCodeType == BLOCK_CODELINE_TYPE.WHILE 
            || blockCodeType == BLOCK_CODELINE_TYPE.TRY
            // || blockCodeType == BLOCK_CODELINE_TYPE.ELSE 
            // || blockCodeType == BLOCK_CODELINE_TYPE.ELIF
            // || blockCodeType == BLOCK_CODELINE_TYPE.FOR_ELSE 
            // || blockCodeType == BLOCK_CODELINE_TYPE.EXCEPT 
            // || blockCodeType == BLOCK_CODELINE_TYPE.FINALLY
            // || blockCodeType == BLOCK_CODELINE_TYPE.LAMBDA
            
            || blockCodeType == BLOCK_CODELINE_TYPE.CONTINUE
            || blockCodeType == BLOCK_CODELINE_TYPE.BREAK
            || blockCodeType == BLOCK_CODELINE_TYPE.PASS
            || blockCodeType == BLOCK_CODELINE_TYPE.RETURN) {
            blockContainer = $(`.vp-apiblock-tab-navigation-node-subblock-2-body-inner`);
  
        }  else  {
            // if (blockCodeType == BLOCK_CODELINE_TYPE.BLANK) {
            //     $(rootDomElement).css('background-color', 'rgb(229, 229, 229)');
            // } 
            blockContainer = $(`.vp-apiblock-tab-navigation-node-subblock-3-body-inner`);
        }
        blockContainer.append(rootDomElement);
    }

    CreateBlockBtn.prototype.bindBtnDragEvent = function() {
        var thisBlockBtn = this;
        var rootDom = this.getBlockMainDom();
        var blockContainerThis = this.getBlockContainerThis();
        var blockCodeLineType = this.getBlockCodeLineType();

        var currCursorX = 0;
        var currCursorY = 0;
        var newPointX = 0;
        var newPointY = 0;

        var selectedBlockDirection = null;
        var shadowBlock = null;
        var newBlock = null;
        var rootBlock =  null; 

        var thisBlockBtnWidth = 0;

        var $shadowBlockMainDom = null;
        $(rootDom).draggable({ 
            addClass: '.vp-dragable-btn',
            appendTo: VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MAIN,
            containment: VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MAIN,
            cursor: 'move', 
            helper: 'clone',
            start: function(event, ui) {

                rootBlock = blockContainerThis.getRootBlock();
                if (rootBlock) {
                    /** shadow 블럭 생성 */
                    shadowBlock = new ShadowBlock(blockContainerThis, blockCodeLineType, []);
                    $shadowBlockMainDom = $(shadowBlock.getBlockMainDom());

                    var containerDom = blockContainerThis.getBlockContainerDom();
                    $(shadowBlock.getBlockMainDom()).css(STR_DISPLAY,STR_NONE);
                    $(containerDom).append(shadowBlock.getBlockMainDom());
                }

                /** height 길이 결정 */
                var blockList = blockContainerThis.getBlockList();
                blockList.forEach(block => {
                    var holderBlock = block.getHolderBlock();
                    if ( holderBlock != null ) {
                        block.calculateLeftHolderHeightAndSet();
                        var distance = block.getTempBlockLeftHolderHeight();
                        $(block.getBlockLeftHolderDom()).css(STR_HEIGHT, distance);
                    }
                });
                ({ width: thisBlockBtnWidth } = thisBlockBtn.getBlockMainDomPosition());
            },
            drag: async function(event, ui) {  
       
                currCursorX = event.clientX; 
                currCursorY = event.clientY; 

                /** 만약  아래 로직에서 + thisBlockWidth + 10이 없다면 마우스 커서 오른쪽으로 이동 됨*/
                newPointX = currCursorX - $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD).offset().left  + thisBlockBtnWidth + 10 ;
                newPointY = currCursorY - $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD).offset().top ;

                /** drag Block 생성 버튼 마우스 커서 왼쪽 위로 이동 구현 */
                ui.position = {
                    top: newPointY,
                    left: newPointX
                };

                /** 블록 전체를 돌면서 drag하는 Block 생성 버튼과 Editor위에 생성된 블록들과 충돌 작용  */
                var blockList = blockContainerThis.getBlockList();
 
                blockList.forEach( (block,index) => {
                // for await (var block of blockList) {

                    var { x: blockX 
                          , y: blockY
                          , width: blockWidth
                          , height: blockHeight } = block.getBlockMainDomPosition();
    
                    var blockLeftHolderHeight = block.getTempBlockLeftHolderHeight() == 0 
                                                                            ? blockHeight 
                                                                            : block.getTempBlockLeftHolderHeight();
           
                    /** 블럭 충돌에서 벗어나는 로직 */
                    if ( (blockX > currCursorX 
                        || currCursorX > (blockX + blockWidth)
                        || blockY  > currCursorY 
                        || currCursorY > (blockY + blockHeight + blockHeight + blockHeight + blockLeftHolderHeight) ) ) {
                        block.renderBlockHolderShadow_2(STR_NONE);
                    }


                    /** 블럭 충돌 left holder shadow 생성 로직 */
                    if ( blockX < currCursorX
                        && currCursorX < (blockX + blockWidth )
                        && blockY  < currCursorY
                        && currCursorY < (blockY + blockHeight + blockLeftHolderHeight) ) {     
                   
                        block.renderBlockHolderShadow_2(STR_BLOCK);   

                        var holderBlock = block.getHolderBlock();
                        if ( holderBlock != null ) {
                             block._renderBlockLeftHolderListHeight();
                        }
                    }

                    /** 블럭 충돌 시 */
                    if ( blockX < currCursorX
                        && currCursorX < (blockX + blockWidth )
                        && blockY  < currCursorY
                        && currCursorY < (blockY + blockHeight  + blockHeight) ) {

                        var holderBlock = block.getHolderBlock();
                        if ( holderBlock != null ) {
                            block._renderBlockLeftHolderListHeight();
                        }

                        /** Class & def or Controls Block들은
                         *  holderBlock을 가지고 있다 */
                        var holderBlock = block.getHolderBlock();
                        if ( holderBlock != null ) {
                            selectedBlockDirection = BLOCK_DIRECTION.INDENT;
                        } else {
                            selectedBlockDirection = BLOCK_DIRECTION.DOWN; 
                        }

                        block.makeShadowDomList( shadowBlock, selectedBlockDirection);
                    } else {

                        var containerDom = blockContainerThis.getBlockContainerDom();
                        var containerDomRect = $(containerDom)[0].getBoundingClientRect();
                        var { x: containerDomX, 
                              y: containerDomY, 
                              width: containerDomWidth, 
                              height: containerDomHeight} = containerDomRect;
                

                        /** board에 있는 어떠한 block에 닿았을 때 */
                        if ( containerDomX < currCursorX
                            && currCursorX < (containerDomX + containerDomWidth)
                            && containerDomY  < currCursorY
                            && currCursorY < (containerDomY + containerDomHeight) ) {  

                        /** board에 있는 어떠한 block에도 닿지 않았을 때 */
                        } else {
                            $(shadowBlock.getBlockMainDom()).css(STR_DISPLAY, STR_NONE);
                            shadowBlock.setSelectBlock(null); 
                        }
                    }
                })
                // );
            },
            stop: function() {
                 /** 현재 drag하는 Block 생성 버튼 위치 구현 */
                blockContainerThis.setEventClientY(currCursorY);

                var selectedBlock = null;
                if (shadowBlock) {
                    selectedBlock = shadowBlock.getSelectBlock();
                    $shadowBlockMainDom.remove();
                }
   
                /** Board에 생성된 Block에 연결할 경우 */
                if (selectedBlock != null) {
                    newBlock = blockContainerThis.createBlock(blockCodeLineType );
                    selectedBlock.appendBlock(newBlock, selectedBlockDirection);
                    newBlock.renderEditorScrollTop();

                /** Board에 생성된 Block에 연결하지 못한 경우 
                 *  즉 아무대도 연결하지 못하고 생성한 경우
                */
                }  else { 
                    var blockList = blockContainerThis.getBlockList();
                    /** 
                     * Board에 생성된 Block이 1개도 없을 때
                     */
                    if (blockList.length == 0) {
                    
                        newBlock = blockContainerThis.createBlock( blockCodeLineType );

                        var _containerDom = blockContainerThis.getBlockContainerDom();
                        $(_containerDom).remove();

                        var containerDom = document.createElement(STR_DIV);
                        containerDom.classList.add(VP_CLASS_BLOCK_CONTAINER);
                        blockContainerThis.setBlockContainerDom(containerDom);

                        $(containerDom).css(STR_TOP,`${NUM_DEFAULT_POS_Y}${STR_PX}`);
                        $(containerDom).css(STR_LEFT,`${NUM_DEFAULT_POS_X}${STR_PX}`);

                        blockContainerThis.reRenderBlockList();
                        blockContainerThis.renderBlockLineNumberInfoDom(true);

                        $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD).append(containerDom);

                        /** 최초 생성된 root 블럭 set root direction */
                        newBlock.setDirection(BLOCK_DIRECTION.ROOT);
                    /** 
                     * Board에 생성된 Block이 적어도 1개는 있을 때
                     */
                    } else {
                        var rootBlock = blockContainerThis.getRootBlock();
                        newBlock = blockContainerThis.createBlock( blockCodeLineType );
                        var currentBlock = blockContainerThis.getRootToLastBottomBlock();

                        /** Class & def or Controls Block들은
                         *  holderBlock을 가지고 있다 */
                        var holderBlock = rootBlock.getHolderBlock();
                        if ( holderBlock != null ) {
                            if (currentBlock == null) {
                                rootBlock.getHolderBlock().appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                            } else {
                                currentBlock.appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                            }
                        } else {
                            if (currentBlock == null) {
                                rootBlock.appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                            } else {
                                currentBlock.appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                            }
                        }
    
                        newBlock.renderEditorScrollTop(true);
                    }
                }

                blockContainerThis.calculateDepthFromRootBlockAndSetDepth();
          

                blockContainerThis.reRenderBlockList();
                blockContainerThis.renderBlockLineNumberInfoDom(true);

                blockContainerThis.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.BUTTONS);

                blockContainerThis.bindCodeBlockInputFocus(newBlock, blockCodeLineType);

                newBlock.renderSelectedMainBlockBorderColor();
                
                blockContainerThis.setSelectedBlock(newBlock);
                blockContainerThis.renderBlockOptionTab();

                var blockList = blockContainerThis.getBlockList();
                blockList.forEach(block => {

                    block.renderBlockHolderShadow_2(STR_NONE);
                    block.renderFontWeight300();
                    block.renderCodeLineDowned();
                    $(block.getBlockMainDom()).find(VP_CLASS_PREFIX + VP_CLASS_BLOCK_DELETE_BTN).remove();
                    $(block.getBlockMainDom()).find(VP_CLASS_PREFIX + VP_CLASS_BLOCK_OPTION_BTN).remove();
                    $(block.getBlockMainDom()).find(VP_CLASS_PREFIX + 'vp-apiblock-elif-else-container-button').remove();

                    block.renderResetColor();
                });

                /** 서브 버튼 생성 */
                newBlock.createSubButton();
                
                /** 옵션 페이지 리셋  */
                newBlock.resetOptionPage();
        
                /** 옵션 페이지 다시 오픈 */
                blockContainerThis.renderBlockOptionTab();
                newBlock.renderOptionPage();


                /** 자식 하위 Depth Block Border 색칠 */
                var childLowerDepthBlockList = newBlock.getChildLowerDepthBlockList();
                childLowerDepthBlockList.forEach(block => {
                    block.renderSelectedBlockBorderColor();
                    block.renderFontWeight700();
                });

                shadowBlock = null;
                newBlock = null;


            }
        });
    }

    return CreateBlockBtn;
});
