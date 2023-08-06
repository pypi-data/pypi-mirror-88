define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'

    , '../api.js'    
    , '../config.js'
    , '../constData.js'
    , '../createBlockBtn.js'
    
], function ( $, vpCommon, vpConst, sb, api, config, constData, createBlockBtn) {
    const { ControlToggleInput
            , JQueryPutCursorAtEnd } = api;

    const { PROCESS_MODE } = config;
    const { BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , FOCUSED_PAGE_TYPE

            , VP_ID_PREFIX
            , VP_ID_APIBLOCK_VIEWDEPTH
            , VP_ID_APIBLOCK_LINENUMBER_ASC
            , VP_ID_APIBLOCK_DELETE_BLOCK_ALL
            , VP_ID_APIBLOCK_CLOSE

            , VP_CLASS_PREFIX
            , VP_CLASS_APIBLOCK_BOARD
            , VP_CLASS_APIBLOCK_MENU_BTN
            , VP_CLASS_APIBLOCK_OPTION_TAB
            , VP_CLASS_APIBLOCK_TAB_NAVIGATION_NODE_OPTION_TITLE_SAPN
            , VP_CLASS_APIBLOCK_BOTTOM_TAB_VIEW
            , VP_CLASS_APIBLOCK_OPTION_TAB_CHILDS_OPTION
            , VP_CLASS_APIBLOCK_BOTTOM_OPTIONAL_TAB_VIEW

            , STR_OPTION 
            , STR_CLICK
            , STR_OPACITY } = constData;

    var apiBlockMenuInit = function(blockContainer) {
        var apiBlockMenuBarDom ;


        /** board 메뉴 박스 생성 클릭 이벤트 함수 */
        /** FIXME: 추후 개선 */
        $(document).off(STR_CLICK, vpCommon.wrapSelector(vpCommon.formatString(".{0}", VP_CLASS_APIBLOCK_MENU_BTN)));
        $(document).on(STR_CLICK, vpCommon.wrapSelector(vpCommon.formatString(".{0}", VP_CLASS_APIBLOCK_MENU_BTN)), function(event) {
         
            var isMenubarOpen = blockContainer.getIsMenubarOpen();
            if (isMenubarOpen == true) {
                    blockContainer.setIsMenubarOpen(false);   
                    /** board 메뉴 박스 삭제 */
                $(apiBlockMenuBarDom).remove(); 
            
            } else {
                var isShowDepth = blockContainer.getIsShowDepth();
                var isShowDepthStr = '';
                if (isShowDepth == true) {
                    isShowDepthStr = 'off';
                } else {
                    isShowDepthStr = 'on';
                }
                blockContainer.setIsMenubarOpen(true);
                    /** board 메뉴 박스 생성 */
                renderThisComponent(isShowDepthStr);
            }
            event.stopPropagation();
        });
 

        /** Block Depth 보이기 안보이기 on/off 이벤트 함수 */
        $(document).on(STR_CLICK, vpCommon.wrapSelector(vpCommon.formatString("#{0}", VP_ID_APIBLOCK_VIEWDEPTH)), function(event) {
            
            /** board 메뉴 박스 삭제 */
            $(apiBlockMenuBarDom).remove(); 

            var blockList = blockContainer.getBlockList();
            var isShowDepth = blockContainer.getIsShowDepth();
            /** Block depth 보이기 on*/
            if (isShowDepth == true) {
                blockList.forEach(block => {
                    $(block.getBlockDepthInfoDom()).css(STR_OPACITY, 0);
                });
                $(vpCommon.wrapSelector(VP_ID_PREFIX + VP_ID_APIBLOCK_VIEWDEPTH)).text(`View depth on`);
                blockContainer.setIsShowDepth(false);
            /** Block depth 안 보이기 off */             
            } else {
                blockList.forEach(block => {
                    $(block.getBlockDepthInfoDom()).css(STR_OPACITY, 1);
                });
                $(vpCommon.wrapSelector(VP_ID_PREFIX + VP_ID_APIBLOCK_VIEWDEPTH)).text(`View depth off`);
                blockContainer.setIsShowDepth(true);
            }
    
            blockContainer.setIsMenubarOpen(false);
            event.stopPropagation();
        });


        /** Block line number 오름차순 정렬 이벤트 함수 */
        $(document).on(STR_CLICK, vpCommon.wrapSelector(vpCommon.formatString("#{0}", VP_ID_APIBLOCK_LINENUMBER_ASC)), function(event) {
        
            /** board 메뉴 박스 삭제 */
            $(apiBlockMenuBarDom).remove(); 

            var rootBlock = blockContainer.getRootBlock();
            if (rootBlock) {
                blockContainer.renderBlockLineNumberInfoDom(true);
            }
        
            blockContainer.setIsMenubarOpen(false);
            event.stopPropagation();
        });


        // /** Opiton page toggle 이벤트 함수 */
        // $(document).on(STR_CLICK, vpCommon.wrapSelector(vpCommon.formatString("#{0}", 'vp_apiblock_toggle_optionpage')), function(event) {
      
        //     /** board 메뉴 박스 삭제 */
        //     $(apiBlockMenuBarDom).remove(); 

        //     var isOptionPageOpen = blockContainer.getIsOptionPageOpen();
        //     if (isOptionPageOpen == true) {

        //         $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css('width','0px');
        //         $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).animate({width:'toggle'});
        //         $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MENU_BTN)).css('right', '385px');
                
        //         blockContainer.setIsOptionPageOpen(false);   
        //     } else {
      
        //         $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css('width','380px');
        //         $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).animate({width:'toggle'});
        //         $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MENU_BTN)).css('right', '5px');

        //         blockContainer.setIsOptionPageOpen(true);   
        //     }
        //     // clickMenuBar();
        //     event.stopPropagation();
        // });
        $(document).on(STR_CLICK, vpCommon.wrapSelector(vpCommon.formatString("#{0}", 'vp_apiblockSaveMetadata')), function(event) {
            /** board 메뉴 박스 삭제 */
            $(apiBlockMenuBarDom).remove(); 
            blockContainer.setIsMenubarOpen(false);
            
            blockContainer.saveAPIBlockMetadata(true);
            event.stopPropagation();
        });

        $(document).on(STR_CLICK, vpCommon.wrapSelector(vpCommon.formatString("#{0}", 'vp_apiblockLoadMetadata')), function(event) {
            /** board 메뉴 박스 삭제 */
            $(apiBlockMenuBarDom).remove(); 
            blockContainer.setIsMenubarOpen(false);
            
            blockContainer.loadAPIBlockMetadata();
            
            event.stopPropagation();
        });

        // $(document).on(STR_CLICK, vpCommon.wrapSelector(vpCommon.formatString("#{0}", 'vp_apiblockUndo')), function(event) {
        //     /** board 메뉴 박스 삭제 */
        //     $(apiBlockMenuBarDom).remove(); 
        //     blockContainer.setIsMenubarOpen(false);
            
        //     blockContainer.undoBlockList();
        //     blockContainer.reRenderBlockList();
        //     blockContainer.renderBlockLineNumberInfoDom(true);

        //     /** 옵션 페이지 리셋  */
        //     $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_TAB_NAVIGATION_NODE_OPTION_TITLE_SAPN)).html(STR_OPTION);
        //     $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOTTOM_TAB_VIEW)).empty();

        //     $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB_CHILDS_OPTION)).remove();
        //     $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOTTOM_OPTIONAL_TAB_VIEW)).empty();

        //     /** 옵션 페이지 다시 오픈 */
        //     blockContainer.renderBlockOptionTab();
        //     // thisBlock.renderOptionPage();
        //     event.stopPropagation();
        // });

        // $(document).on(STR_CLICK, vpCommon.wrapSelector(vpCommon.formatString("#{0}", 'vp_apiblockRedo')), function(event) {
        //     /** board 메뉴 박스 삭제 */
        //     $(apiBlockMenuBarDom).remove(); 
        //     blockContainer.setIsMenubarOpen(false);
            
        //     blockContainer.redoBlockList();
        //     blockContainer.reRenderBlockList();
        //     blockContainer.renderBlockLineNumberInfoDom(true);
        //     /** 옵션 페이지 리셋  */
        //     $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_TAB_NAVIGATION_NODE_OPTION_TITLE_SAPN)).html(STR_OPTION);
        //     $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOTTOM_TAB_VIEW)).empty();

        //     $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB_CHILDS_OPTION)).remove();
        //     $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOTTOM_OPTIONAL_TAB_VIEW)).empty();
     

        //     /** 옵션 페이지 다시 오픈 */
        //     blockContainer.renderBlockOptionTab();
        //     // thisBlock.renderOptionPage();
        //     event.stopPropagation();
        // });
  
        /** Board위에 존재하는 모든 Block 삭제 이벤트 함수 */
        $(document).on(STR_CLICK, vpCommon.wrapSelector(vpCommon.formatString("#{0}", VP_ID_APIBLOCK_DELETE_BLOCK_ALL)), function(event) {
       
            /** board 메뉴 박스 삭제 */
            $(apiBlockMenuBarDom).remove(); 
      
            var rootBlock = blockContainer.getRootBlock();
            if (rootBlock) {
                rootBlock.deleteBlock();
                rootBlock.resetOptionPage();
            
                blockContainer.setBlockList([]);
                blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.EDITOR);
                $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).animate({
                    scrollTop: 0 
                }, 100);
            }
            
            blockContainer.setIsMenubarOpen(false);
            event.stopPropagation();
        });


        /** board 메뉴 닫기 이벤트 함수 */
        $(document).on(STR_CLICK, vpCommon.wrapSelector(vpCommon.formatString("#{0}", VP_ID_APIBLOCK_CLOSE)), function(event) {

            /** board 메뉴 박스 삭제 */
            $(apiBlockMenuBarDom).remove(); 

            blockContainer.setIsMenubarOpen(false);
            event.stopPropagation();
        });


        /** board 메뉴 창을 클릭하면 메뉴를 닫음
         */
        $(document).on(STR_CLICK, vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.VP_NOTE_EXTRA_MENU_CONTAINER)), function(event) {

            
            /** board 메뉴 박스 삭제 */
            $(apiBlockMenuBarDom).remove(); 

            blockContainer.setIsMenubarOpen(false);
            event.stopPropagation();
        });

    
        $(document).on(STR_CLICK, function(event) {
            // if (!event.target.id){
            $(apiBlockMenuBarDom).remove(); 

            blockContainer.setIsMenubarOpen(false);
            event.stopPropagation();
            // }
            // console.log('event.target.id', event.target.id);
        });

        /** board 메뉴 박스 렌더링 */
        var renderThisComponent = function(isShowDepthStr) {
            // vpConst.VP_NOTE_EXTRA_MENU_BTN
            var sbAPIBlockMenu = new sb.StringBuilder();
            sbAPIBlockMenu.appendFormatLine("<div id='{0}'  style='{1}'>", vpConst.VP_NOTE_EXTRA_MENU_BTN, 'display: block;');
            sbAPIBlockMenu.appendFormatLine("<div id='{0}' >", vpConst.VP_NOTE_EXTRA_MENU_CONTAINER, );
            sbAPIBlockMenu.appendFormatLine("<ul class='{0}'>", vpConst.VP_NOTE_EXTRA_MENU_LIST);
            sbAPIBlockMenu.appendFormatLine("<li class='{0}' id='{1}'>", vpConst.VP_EXCEPT_BIND, VP_ID_APIBLOCK_VIEWDEPTH);
            sbAPIBlockMenu.appendFormatLine("{0}</li>", 'View depth ' + isShowDepthStr);

            sbAPIBlockMenu.appendFormatLine("<hr class='{0}'/>", vpConst.VP_NOTE_EXTRA_MENU_LINE);

            sbAPIBlockMenu.appendFormatLine("<li class='{0}' id='{1}'>", vpConst.VP_EXCEPT_BIND, VP_ID_APIBLOCK_LINENUMBER_ASC);
            sbAPIBlockMenu.appendFormatLine("{0}</li>", 'Line number asc');

            sbAPIBlockMenu.appendFormatLine("<hr class='{0}'/>", vpConst.VP_NOTE_EXTRA_MENU_LINE);

            // sbAPIBlockMenu.appendFormatLine("<li class='{0}' id='{1}'>", vpConst.VP_EXCEPT_BIND, 'vp_apiblockSaveMetadata');
            // sbAPIBlockMenu.appendFormatLine("{0}</li>", 'Save metadata');

            // sbAPIBlockMenu.appendFormatLine("<hr class='{0}'/>", vpConst.VP_NOTE_EXTRA_MENU_LINE);

            // sbAPIBlockMenu.appendFormatLine("<li class='{0}' id='{1}'>", vpConst.VP_EXCEPT_BIND, 'vp_apiblockLoadMetadata');
            // sbAPIBlockMenu.appendFormatLine("{0}</li>", 'Load metadata');

            // sbAPIBlockMenu.appendFormatLine("<hr class='{0}'/>", vpConst.VP_NOTE_EXTRA_MENU_LINE);
            // sbAPIBlockMenu.appendFormatLine("<li class='{0}' id='{1}'>", vpConst.VP_EXCEPT_BIND, 'vp_apiblock_toggle_optionpage');
            // sbAPIBlockMenu.appendFormatLine("{0}</li>", 'Toggle Option');

            // sbAPIBlockMenu.appendFormatLine("<hr class='{0}'/>", vpConst.VP_NOTE_EXTRA_MENU_LINE);

            // sbAPIBlockMenu.appendFormatLine("<li class='{0}' id='{1}'>", vpConst.VP_EXCEPT_BIND, 'vp_apiblockUndo');
            // sbAPIBlockMenu.appendFormatLine("{0}</li>", 'Undo BlockList');

            // // sbAPIBlockMenu.appendFormatLine("<hr class='{0}'/>", vpConst.VP_NOTE_EXTRA_MENU_LINE);
            // sbAPIBlockMenu.appendFormatLine("<li class='{0}' id='{1}'>", vpConst.VP_EXCEPT_BIND, 'vp_apiblockRedo');
            // sbAPIBlockMenu.appendFormatLine("{0}</li>", 'Redo BlockList');

            // sbAPIBlockMenu.appendFormatLine("<hr class='{0}'/>", vpConst.VP_NOTE_EXTRA_MENU_LINE);

            sbAPIBlockMenu.appendFormatLine("<li class='{0}' id='{1}'>", vpConst.VP_EXCEPT_BIND, VP_ID_APIBLOCK_DELETE_BLOCK_ALL);
            sbAPIBlockMenu.appendFormatLine("{0}</li>", 'Delete all block');

            sbAPIBlockMenu.appendFormatLine("<hr class='{0}'/>", vpConst.VP_NOTE_EXTRA_MENU_LINE);

            sbAPIBlockMenu.appendFormatLine("<li class='{0}' id='{1}'>", vpConst.VP_EXCEPT_BIND, VP_ID_APIBLOCK_CLOSE);
            sbAPIBlockMenu.appendFormatLine("{0}</li>", 'Close');
            sbAPIBlockMenu.appendLine("</ul>");
            sbAPIBlockMenu.appendLine("</div>");
            sbAPIBlockMenu.appendLine("</div>");
            /** board 메뉴 박스 생성 */
            apiBlockMenuBarDom = $(sbAPIBlockMenu.toString());

            /** board 메뉴 버튼아래에 메뉴 박스 생성 */
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MENU_BTN)).append(apiBlockMenuBarDom);
        }
    }

    return apiBlockMenuInit;

});