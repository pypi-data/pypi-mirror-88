
define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpXMLHandler'
    , 'nbextensions/visualpython/src/common/component/vpAccordionBox'
    , 'nbextensions/visualpython/src/common/component/vpLineNumberTextArea'
    , 'nbextensions/visualpython/src/common/component/vpIconInputText'
    , 'nbextensions/visualpython/src/common/vpFuncJS'
    , '../../api.js'    
    , '../../config.js'
    , '../../constData.js'
    , '../../blockRenderer.js'
    , '../base/index.js'

], function ( $, vpCommon, vpConst, sb, xmlHandler, vpAccordionBox, vpLineNumberTextArea,vpIconInputText, vpFuncJS

              , api
              , config
              , constData
              , blockRenderer

              , baseComponent ) {

    const { SetTextareaLineNumber_apiBlock } = api;
    const { PROCESS_MODE } = config;
    const { RenderInputRequiredColor
            , RenderCodeBlockInputRequired } = blockRenderer;

    const { BLOCK_CODELINE_TYPE
            , STR_CHANGE_KEYUP_PASTE

            , STR_NULL
            , STR_ONE_SPACE 
            , STR_BREAK
            , STR_CONTINUE
            , STR_PASS
            , STR_INPUT_YOUR_CODE
            , STR_COLOR

            , STATE_customCodeLine
            , COLOR_BLACK
            , COLOR_GRAY_input_your_code

            , VP_ID_PREFIX
            , VP_ID_APIBLOCK_OPTION_CODE_ARG

            , VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED } = constData;
    const { MakeOptionContainer } = baseComponent;
    /**
     * @param {Block} thatBlock Block
     * @param {string} optionPageSelector  Jquery 선택자
     */
    var InitCodeBlockOption = function(thatBlock, optionPageSelector) {
        var uuid = thatBlock.getUUID();
        let xmlLibraries;
        let libraryLoadComplete = false;
        let loadedFuncJS;
        let apiBlockJS;
        let generatedCode;
        let generatedMetaData;
        let loadedFuncID;
        var events;
        let nodeIndex = 0;
        let librarySearchComplete = new Array();
        let searchBoxUUID;
        try {
            // events 에 대한 예외 발생 가능할 것으로 예상.
            events = requirejs('base/js/events');
        } catch (err) {
            if (window.events === undefined) {
                var Events = function () { };
                window.events = $([new Events()]);
            }
            events = window.events;
        }
            /**
     * 노트 노드 바로 실행
     * @param {object} trigger 이벤트 트리거 객체
     */
    var runLibraryOnNote = function(trigger) {
        var gCode = decodeURIComponent($(trigger).children(vpCommon.formatString(".{0}", vpConst.NOTE_NODE_GENERATE_CODE)).val());

        vpFuncJS.VpFuncJS.prototype.cellExecute(gCode, true);
    }
        var getOptionPageURL = function(funcID) {
            var sbURL = new sb.StringBuilder();
            
            sbURL.append(Jupyter.notebook.base_url);
            sbURL.append(vpConst.BASE_PATH);
            sbURL.append(vpConst.SOURCE_PATH);
            // 함수 경로 바인딩
            var optionData = $(xmlLibraries.getXML()).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_ID_ATTR + "=" + funcID + "]");
            var filePath = $(optionData).find(vpConst.LIBRARY_ITEM_FILE_URL_NODE).text();
            
            // 경로가 조회되지 않는 경우
            if (filePath === undefined || filePath === "") {
                alert("Function id not founded!");
                return "";
            }
    
            sbURL.append(filePath);
            return sbURL.toString();
        }
    
        /**
         * load api block
         */
        var loadApiBlock = function() {
            // library 정보 로드 종료되지 않으면 이벤트로 등록
            if (!libraryLoadComplete) {
                events.on('library_load_complete.vp', loadApiBlock);
                return;
            }

            events.off('library_load_complete.vp', loadApiBlock);
            var loadUrl = getOptionPageURL("api_block");
            // 옵션 페이지 url 로딩이 정상처리 된 경우 js 파일 로드
            if (loadUrl !== "") {
                // 옵션 로드
                requirejs([loadUrl], function (loaded) {
                    loaded.initOption(apiBlockLoadCallback);
                });
            }
        }

        var addAutoCompleteItem = function(item) {
            // 이미 등록된 항목은 제외한다.
            if (!librarySearchComplete.includes(item)) {
                librarySearchComplete.push(item);
            }
        }
        var setLibraryLoadComplete = function() {
            libraryLoadComplete = true;
            events.trigger('library_load_complete.vp');
        }
        var librariesBind = function(node, container) {
        
            $(node).children(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_TYPE_ATTR + "=" + vpConst.LIBRARY_ITEM_TYPE_PACKAGE + "]").each(function() {
                var thisNode = $(this);
                var accboxTopGrp;
                if ($(thisNode).attr(vpConst.LIBRARY_ITEM_DEPTH_ATTR) == 0) {
                    accboxTopGrp = makeLibraryTopGroupBox($(thisNode));
                    
                    $(container).append(accboxTopGrp.toTagString());
                }
            });
        }
        var bindSearchAutoComplete = function() {
            $(xmlLibraries.getXML()).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_TYPE_ATTR + "=" + vpConst.LIBRARY_ITEM_TYPE_FUNCTION + "]").each(function() {
                addAutoCompleteItem($(this).attr(vpConst.LIBRARY_ITEM_NAME_ATTR));
                $(this).attr(vpConst.LIBRARY_ITEM_TAG_ATTR).split(",").forEach(function(tag) {
                    addAutoCompleteItem(tag.trim());
                });
            });
    
            $(vpCommon.wrapSelector(vpCommon.formatString(".{0} input", searchBoxUUID))).autocomplete({
                source: librarySearchComplete
                , classes: {
                    "ui-autocomplete": "vp-search-autocomplete"
                  }
            });
        }
        var libraryLoadCallback = function(container) {
            setLibraryLoadComplete();
            librariesBind($(xmlLibraries.getXML()).children(vpConst.LIBRARY_ITEM_WRAP_NODE), container);
            
            bindSearchAutoComplete();
        };

        var loadLibraries = function(container) {
            var libraryURL = window.location.origin + vpConst.PATH_SEPARATOR + vpConst.BASE_PATH + vpConst.DATA_PATH + vpConst.VP_LIBRARIES_XML_URL;
            xmlLibraries = new xmlHandler.VpXMLHandler(libraryURL);
            xmlLibraries.loadFile(libraryLoadCallback, container);
        }

        /**
         * 최상위 패키지는 아코디언 박스로 생성한다.
         * @param {xmlNode} topGrpNode 최상위 페키지
         */
        var makeLibraryTopGroupBox = function(topGrpNode) {
            var accBox = new vpAccordionBox.vpAccordionBox($(topGrpNode).attr(vpConst.LIBRARY_ITEM_NAME_ATTR), false, true);

            // 추가 클래스 설정
            accBox.addClass(vpConst.ACCORDION_GRAY_BGCOLOR);
            accBox.addClass(vpConst.ACCORDION_SMALL_ARROW);

            // 속성 부여
            accBox.addAttribute(vpConst.LIBRARY_ITEM_DATA_ID, $(topGrpNode).attr(vpConst.LIBRARY_ITEM_ID_ATTR));

            // 자식 그룹 노드 생성
            accBox.appendContent(makeLibraryListsGroupNode(topGrpNode));
            
            return accBox;
        }

        /**
         * api list item 클릭
         */
        $(document).on("click", vpCommon.wrapSelector(vpCommon.formatString(".{0} li", vpConst.LIST_ITEM_LIBRARY)), function(evt) {
            evt.stopPropagation();
            if ($(this).hasClass(vpConst.LIST_ITEM_LIBRARY_GROUP)) {
                toggleApiListSubGroupShow($(this));
            } else if ($(this).hasClass(vpConst.LIST_ITEM_LIBRARY_FUNCTION)) {
                loadOption($(this).data(vpConst.LIBRARY_ITEM_DATA_ID.replace(vpConst.TAG_DATA_PREFIX, "")), optionPageLoadCallback);
            }
        });

        /**
         * api list 그룹 하위 표시 토글
         * @param {object} trigger 이벤트 트리거 객체
         */
        var toggleApiListSubGroupShow = function(trigger) {
            $(trigger).parent().children(vpCommon.formatString("li.{0}", vpConst.LIST_ITEM_LIBRARY_GROUP)).not($(trigger)).find(vpCommon.formatString(".{0}", vpConst.LIST_ITEM_LIBRARY)).hide();
            $(trigger).children(vpCommon.formatString(".{0}", vpConst.LIST_ITEM_LIBRARY)).toggle();
            
            // 하이라이트 처리
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.API_LIST_LIBRARY_LIST_CONTAINER)))
                    .find(vpCommon.formatString(".{0}", vpConst.COLOR_FONT_ORANGE))
                    .not($(trigger)).removeClass(vpConst.COLOR_FONT_ORANGE);
            $(trigger).addClass(vpConst.COLOR_FONT_ORANGE);
        }

        /**
         * 옵션 페이지 로드 완료 callback.
         * @param {funcJS} funcJS 옵션 js 객체
         */
        var optionPageLoadCallback = function(funcJS) {
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_LOAD_AREA))).empty();
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_NAVIGATOR_INFO_PANEL),
                vpCommon.formatString(".{0}", vpConst.OPTION_NAVIGATOR_INFO_NODE))).remove();
            $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER)).children(vpConst.OPTION_PAGE).remove();

            // load 옵션 변경시 기존 옵션 이벤트 언바인드 호출.
            if (loadedFuncJS != undefined) {
                loadedFuncJS.unbindOptionEvent();
            }
            loadedFuncJS = funcJS;

            var naviInfoTag = makeOptionPageNaviInfo($(xmlLibraries.getXML()).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_ID_ATTR + "=" + loadedFuncID + "]"));
            // FIXME: funcJS 내부 id libraries.xml 과 매칭 필요
            // var naviInfoTag = makeOptionPageNaviInfo($(xmlLibraries.getXML()).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_ID_ATTR + "=" + loadedFuncJS.funcID + "]"));
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_NAVIGATOR_INFO_PANEL))).append(naviInfoTag);

            // metadata 존재하면 load
            if (loadedFuncJS.metadata !== undefined && loadedFuncJS.metadata != "") {
                loadedFuncJS.loadMeta(loadedFuncJS, generatedMetaData);
            }
            makeUpGreenRoomHTML();
            loadedFuncJS.bindOptionEvent();
        }
        /**
         * 그룹 노드 리스트 아이템으로 생성
         * @param {xmlNode} grpNode 그룹 노드
         */
        var makeLibraryListsGroupNode = function(grpNode) {
            var sbGrpNode = new sb.StringBuilder();
            
            sbGrpNode.appendLine(makeLibraryListsFunctionNode(grpNode));
            
            sbGrpNode.appendFormatLine("<ul class='{0}' {1}>", vpConst.LIST_ITEM_LIBRARY, $(grpNode).attr(vpConst.LIBRARY_ITEM_DEPTH_ATTR) > 0 ? "style='display:none;'" : "");

            $(grpNode).children(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_TYPE_ATTR + "=" + vpConst.LIBRARY_ITEM_TYPE_PACKAGE + "]").each(function() {
                sbGrpNode.appendFormatLine("<li class='{0}' {1}='{2}'>{3}"
                    , vpConst.LIST_ITEM_LIBRARY_GROUP, vpConst.LIBRARY_ITEM_DATA_ID, $(this).attr(vpConst.LIBRARY_ITEM_ID_ATTR), $(this).attr(vpConst.LIBRARY_ITEM_NAME_ATTR));
                
                sbGrpNode.appendLine(makeLibraryListsGroupNode($(this)));
                
                sbGrpNode.appendLine("</li>");
            });
            sbGrpNode.appendLine("</ul>");
            
            return sbGrpNode.toString();
        }
        /**
         * 함수 노드 리스트 아이템으로 생성
         * @param {xmlNode} grpNode 그룹 노드
         */
        var makeLibraryListsFunctionNode = function(grpNode) {
            var sbFuncNode = new sb.StringBuilder();

            sbFuncNode.appendFormatLine("<ul class='{0}' {1}>", vpConst.LIST_ITEM_LIBRARY, $(grpNode).attr(vpConst.LIBRARY_ITEM_DEPTH_ATTR) > 0 ? "style='display:none;'" : "");

            $(grpNode).children(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_TYPE_ATTR + "=" + vpConst.LIBRARY_ITEM_TYPE_FUNCTION + "]").each(function() {
                sbFuncNode.appendFormatLine("<li class='{0}' {1}='{2}'>{3}</li>"
                    , vpConst.LIST_ITEM_LIBRARY_FUNCTION, vpConst.LIBRARY_ITEM_DATA_ID, $(this).attr(vpConst.LIBRARY_ITEM_ID_ATTR), $(this).attr(vpConst.LIBRARY_ITEM_NAME_ATTR));
            });

            sbFuncNode.appendLine("</ul>");

            return sbFuncNode.toString();
        }

        /**
         * API List Mode tab page initialize
         * @returns api list tab page
         */
        var apiListPageInit = function() {
            var sbApiListPage = new sb.StringBuilder();

            // 라이브러리 리스트(네비게이터) 영역
            // sbApiListPage.appendFormatLine("<div id='{0}'>", vpConst.API_LIST_LIBRARY_LIST_CONTAINER);
            sbApiListPage.appendFormatLine("<div class='{0}'>",optionPageSelector);
            // 검색 컨트롤 추가
            var searchBox = new vpIconInputText.vpIconInputText();
            searchBox.setIconClass("srch-icon");
            searchBox.setPlaceholder("search");
            sbApiListPage.appendLine(searchBox.toTagString());
            searchBoxUUID = searchBox._UUID;
            
            // 검색 아이콘 클릭 이벤트 바인딩
            searchBox.addEvent("click", "icon", function() { searchAPIList($(this).parent().children("input").val()); });
            searchBox.addEvent("keydown", "text", function(evt) {
                if (evt.keyCode == 13) {
                    evt.preventDefault();
                    searchAPIList($(this).parent().children("input").val());
                }
            });

            sbApiListPage.appendLine("</div>");
            
            // 옵션 로드용 임시 영역
            sbApiListPage.appendFormatLine("<div id='{0}'></div>", vpConst.OPTION_GREEN_ROOM);

            // // 옵션 표시 영역
            // sbApiListPage.appendFormatLine("<div id='{0}' style='display:none;'>", vpConst.OPTION_CONTAINER);

            // // 옵션 컨트롤 영역
            // sbApiListPage.appendFormatLine("<div id='{0}'>", vpConst.OPTION_CONTROL_PANEL);

            // // 옵션 네비 인포 영역
            // sbApiListPage.appendFormatLine("<div id='{0}'></div>", vpConst.OPTION_NAVIGATOR_INFO_PANEL);
            
            // // 로드 옵션 설정창 닫기 버튼
            // sbApiListPage.appendFormatLine("<div id='{0}'></div>", vpConst.CLOSE_OPTION_BUTTON);
            
            // // 옵션 액션 버튼 컨테이너
            // sbApiListPage.appendFormatLine("<div id='{0}'>", vpConst.ACTION_OPTION_BUTTON_PANEL);

            // sbApiListPage.appendFormatLine("<span type='button' class='{0} {1}' id='{2}'>Add</span>"
            //     , vpConst.ACTION_OPTION_BUTTON, vpConst.COLOR_BUTTON_GRAY_WHITE, vpConst.OPTION_BTN_ADD_CELL);

            // sbApiListPage.appendFormatLine("<span type='button' class='{0} {1}' id='{2}'>Run</span>"
            //     , vpConst.ACTION_OPTION_BUTTON, vpConst.COLOR_BUTTON_ORANGE_WHITE, vpConst.OPTION_BTN_RUN_CELL);

            // sbApiListPage.appendFormatLine("<div id='{0}'></div>", vpConst.OPTION_BTN_SAVE_ON_NOTE);
            
            // sbApiListPage.appendLine("</div>");
            
            // sbApiListPage.appendLine("</div>");
            
            // // 로드된 옵션 위치 영역
            // sbApiListPage.appendFormatLine("<div id='{0}'></div>", vpConst.OPTION_LOAD_AREA);

            sbApiListPage.appendLine("</div>");

            return sbApiListPage.toString();
        }

        /**
         * api list 그룹 하위 모두 숨기기
         */
        var closeSubLibraryGroup = function() {
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.API_LIST_LIBRARY_LIST_CONTAINER), 
                vpCommon.formatString(".{0}", vpConst.ACCORDION_CONTENT_CLASS))).children(vpCommon.formatString(".{0}", vpConst.LIST_ITEM_LIBRARY))
                    .find(vpCommon.formatString(".{0}", vpConst.LIST_ITEM_LIBRARY)).hide();
        }

        /**
         * 옵션 페이지 로드
         * @param {String} funcID xml 함수 id
         * @param {function} callback 로드 완료시 실행할 함수
         * @param {JSON} metadata 메타데이터
         */
        var loadOption = function(funcID, callback, metadata) {
            var loadUrl = getOptionPageURL(funcID);
            // 옵션 페이지 url 로딩이 정상처리 된 경우 js 파일 로드
            if (loadUrl !== "") {
                // 옵션 로드
                loadedFuncID = funcID;
                generatedCode = undefined;
                generatedMetaData = metadata;
                requirejs([loadUrl], function (loaded) {
                    loaded.initOption(callback, metadata);
                });
            }
        }
        /**
         * 로드된 함수 경로 바인딩
         * @param {xmlNode} node node for binding
         */
        var makeOptionPageNaviInfo = function(node) {
            var sbNaviInfo = new sb.StringBuilder();
            
            if ($(node).parent().attr(vpConst.LIBRARY_ITEM_DEPTH_ATTR) !== undefined) {
                sbNaviInfo.appendLine(makeOptionPageNaviInfo($(node).parent()));
            }

            sbNaviInfo.appendFormatLine("<span class='{0}' {1}={2}>{3}</span>"
                , vpConst.OPTION_NAVIGATOR_INFO_NODE, vpConst.LIBRARY_ITEM_DATA_ID, $(node).attr(vpConst.LIBRARY_ITEM_ID_ATTR), $(node).attr(vpConst.LIBRARY_ITEM_NAME_ATTR));
                
            return sbNaviInfo.toString();
        }

            /**
         * 로딩된 옵션 페이지 html 처리
         */
        var makeUpGreenRoomHTML = function() {
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_GREEN_ROOM), vpCommon.formatString(".{0}", vpConst.API_OPTION_PAGE))).each(function() {
                $(this).find("h4:eq(0)").hide();
                $(this).find("hr:eq(0)").hide();
                $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_LOAD_AREA))).append($(this));
            });

            openOptionBook();
        }

            /**
         * open api option container
         */
        var openOptionBook = function() {
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.API_LIST_LIBRARY_LIST_CONTAINER))).hide();
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_CONTAINER))).show();
        }

        /**
         * 로드된 옵션 페이지 닫기
         */
        var closeOptionBook = function() {
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.API_LIST_LIBRARY_LIST_CONTAINER))).show();
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_CONTAINER))).hide();
            
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_NAVIGATOR_INFO_PANEL),
                vpCommon.formatString(".{0}", vpConst.OPTION_NAVIGATOR_INFO_NODE))).remove();
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_LOAD_AREA))).children().remove();
        }
            /**
         * 네비 항목 클릭하여 리스트로 이동
         * @param {object} trigger 이벤트 트리거 객체
         */
        var goListOnNavInfo = function(trigger) {
            var obj = $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.API_LIST_LIBRARY_LIST_CONTAINER)))
                .children(vpCommon.formatString("div[{0}={1}]", vpConst.LIBRARY_ITEM_DATA_ID, $(trigger).data(vpConst.LIBRARY_ITEM_DATA_ID.replace(vpConst.TAG_DATA_PREFIX, ""))));

            // 최상위 그룹클릭인 경우
            if (obj.length > 0) {
                // 유니크 타입인경우 다른 아코디언 박스를 닫는다.
                if ($(obj).hasClass("uniqueType")) {
                    $(obj.parent().children(vpCommon.formatString(".{0}", vpConst.ACCORDION_CONTAINER)).not($(obj)).removeClass(vpConst.ACCORDION_OPEN_CLASS));
                }
                $(obj).addClass(vpConst.ACCORDION_OPEN_CLASS);
                // 하위 그룹 닫기
                closeSubLibraryGroup();
                closeOptionBook();
            } else {
                closeSubLibraryGroup();
                obj = $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.API_LIST_LIBRARY_LIST_CONTAINER)))
                    .find(vpCommon.formatString("[{0}={1}]", vpConst.LIBRARY_ITEM_DATA_ID, $(trigger).data(vpConst.LIBRARY_ITEM_DATA_ID.replace(vpConst.TAG_DATA_PREFIX, ""))));
                
                obj.children(vpCommon.formatString(".{0}", vpConst.LIST_ITEM_LIBRARY)).show();
                var objParent = obj.parent();
                for (var loopSafety = 0; loopSafety < 10; loopSafety++) {
                    // 부모 리스트 존재하면 표시
                    if ($(objParent).hasClass(vpConst.LIST_ITEM_LIBRARY)) {
                        $(objParent).show();
                    } else if ($(objParent).hasClass(vpConst.ACCORDION_CONTAINER)) {
                        // 유니크 타입인경우 다른 아코디언 박스를 닫는다.
                        if ($(objParent).hasClass("uniqueType")) {
                            $(objParent.parent().children(vpCommon.formatString(".{0}", vpConst.ACCORDION_CONTAINER)).not($(objParent)).removeClass(vpConst.ACCORDION_OPEN_CLASS));
                        }
                        $(objParent).addClass(vpConst.ACCORDION_OPEN_CLASS);
                    }
                    objParent = $(objParent).parent();
                    
                    // 부모가 api list contianer 이면 종료
                    if ($(objParent).attr("id") == vpConst.API_LIST_LIBRARY_LIST_CONTAINER) {
                        break;
                    }
                }
                closeOptionBook();
            }
        }
        /** Code option 렌더링 */
        var renderThisComponent = function() {
            /** ------------ get state -------------*/
  
            
            /* ------------- string builder render -------------- */
            var optionContainer = MakeOptionContainer();
            // var lineNumberTextArea = new vpLineNumberTextArea.vpLineNumberTextArea(VP_ID_APIBLOCK_OPTION_CODE_ARG + uuid, 
            //                                                                        codeState);                                                                 
            // var lineNumberTextAreaStr = lineNumberTextArea.toTagString();
     
            // optionContainer.append(lineNumberTextAreaStr);
   
            /** 오른쪽 block option 탭에 렌더링된 dom객체 생성 */
            apiListPageInit();
            loadLibraries(optionPageSelector);
            // loadLibraries(vpCommon.formatString("#{0}", vpConst.API_LIST_LIBRARY_LIST_CONTAINER));
            // $(optionPageSelector).append(optionContainer);

            // /** 처음 Code Option 생성시,
            //  *  사용자가 입력한 값을 토대로
            //  *  라인 넘버를 생성하기 위해서 커스터 마이징한 api 사용 */
            // SetTextareaLineNumber_apiBlock(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_CODE_ARG + uuid, codeState);

            // /** Code Option State에 문자열이 1개도 없을 때 */                                                                                   
            // if (codeState == STR_NULL) {
            //     RenderInputRequiredColor(VP_ID_PREFIX + VP_ID_APIBLOCK_OPTION_CODE_ARG + uuid);
            // }       
        }

        renderThisComponent();
    }
    // /**
    //  * load libraries data
    //  * @param {Tag} container loaded libray binding container
    //  */
    // var loadLibraries = function(container) {
    //     var libraryURL = window.location.origin + vpConst.PATH_SEPARATOR + vpConst.BASE_PATH + vpConst.DATA_PATH + vpConst.VP_LIBRARIES_XML_URL;
    //     xmlLibraries = new xmlHandler.VpXMLHandler(libraryURL);
    //     xmlLibraries.loadFile(libraryLoadCallback, container);
    // }
    return InitCodeBlockOption;
});