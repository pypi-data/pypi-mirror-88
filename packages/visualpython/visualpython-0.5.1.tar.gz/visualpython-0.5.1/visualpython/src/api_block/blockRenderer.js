define([
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/StringBuilder'
 
    , './api.js'
    , './constData.js'
    , './component/base/index.js'
 ], function ( vpCommon, sb, 
                api, constData, baseComponent ) {
 
    const { DeleteOneArrayValueAndGet
            , IsCodeBlockType
            , MapNewLineStrToSpacebar } = api;
 
    const { BLOCK_CODELINE_TYPE
            , IMPORT_BLOCK_TYPE
            , IF_BLOCK_CONDITION_TYPE
            , FOCUSED_PAGE_TYPE
            
            , DEF_BLOCK_ARG4_TYPE

            , FOR_BLOCK_ARG3_TYPE
            , WHILE_BLOCK_TYPE 

            , NUM_FONT_WEIGHT_300
            , NUM_FONT_WEIGHT_700
 
            , STR_NULL
            , STR_DIV
            , STR_SELECTED
            , STR_ONE_SPACE
            , STR_ONE_INDENT
            , STR_CHECKED
            
            , STR_BREAK
            , STR_CONTINUE
            , STR_PASS
 
            , STR_INPUT_YOUR_CODE
            , STR_ICON_ARROW_UP
            , STR_ICON_ARROW_DOWN
            , STR_BORDER 
            , STR_DEFAULT
            , STR_CUSTOM
            , STR_TRANSPARENT
 
            , STR_FONT_WEIGHT
            , STR_BORDER_RIGHT
            , STR_BORDER_TOP_LEFT_RADIUS
            , STR_BORDER_BOTTOM_LEFT_RADIUS
            , STR_BORDER_TOP_RIGHT_RADIUS
            , STR_BORDER_BOTTOM_RIGHT_RADIUS
            , STR_3PX
            , STR_SOLID
            , STR_COLOR
            , STR_CLICK
            , STR_COLON_SELECTED
            , STR_CHANGE_KEYUP_PASTE
            , STR_KEYWORD_NEW_LINE

            , VP_CLASS_PREFIX 
 
            , VP_BLOCK_BLOCKCODELINETYPE_CODE
            , VP_BLOCK_BLOCKCODELINETYPE_CLASS_DEF
            , VP_BLOCK_BLOCKCODELINETYPE_CONTROL
 
            , VP_CLASS_BLOCK_CODETYPE_NAME
            , VP_CLASS_APIBLOCK_BOARD
            , VP_CLASS_APIBLOCK_BUTTONS
            , VP_CLASS_APIBLOCK_OPTION_TAB
            , VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED
            , VP_CLASS_APIBLOCK_PARAM_PLUS_BTN
 
            , STATE_classInParamList
            , STATE_className
            , STATE_parentClassName
            
            , STATE_defName
            , STATE_defInParamList
            , STATE_defReturnType

            , STATE_ifCodeLine
            , STATE_isIfElse
            , STATE_isForElse
            , STATE_ifConditionList
            , STATE_elifConditionList
 
            , STATE_elifCodeLine
            , STATE_elifList
 
            , STATE_forCodeLine
            , STATE_forParam 
            , STATE_listforConditionList
            , STATE_listforReturnVar
            , STATE_listforPrevExpression
 
            , STATE_whileCodeLine
            , STATE_whileBlockOptionType
            , STATE_whileArgs
            , STATE_whileConditionList

            , STATE_breakCodeLine
            , STATE_passCodeLine
            , STATE_continueCodeLine
 
            , STATE_baseImportList
            , STATE_customImportList
 
            , STATE_exceptList
            , STATE_exceptCodeLine
            , STATE_exceptConditionList
 
            , STATE_isFinally
 
            , STATE_returnOutParamList
 
            , STATE_customCodeLine
 
            , STATE_propertyCodeLine
 
            , STATE_commentLine
 
            , STATE_lambdaArg1
            , STATE_lambdaArg2List
            , STATE_lambdaArg2m_List
            , STATE_lambdaArg3
            , STATE_lambdaArg4List
 
            , COLOR_GRAY_input_your_code
            , COLOR_FOCUSED_PAGE
            , COLOR_BLACK } = constData;
    const {  MakeOptionPlusButton } = baseComponent;  
    var RenderBlockMainDom = function(thatBlock) {
        var mainDom = document.createElement(STR_DIV);
        mainDom.classList.add('vp-block');
        mainDom.classList.add(`vp-block-${thatBlock.getUUID()}`);
        mainDom.setAttribute("id", `vp_block-${thatBlock.getUUID()}`);
        return mainDom;
    }
    
    var RenderBlockLeftHolderDom = function(thatBlock) {
        var mainDom = document.createElement(STR_DIV);
        mainDom.classList.add('vp-block-left-holder');
        mainDom.setAttribute("id", `vp_block-${thatBlock.getUUID()}`);
        return mainDom;
    }
 
    var RenderBlockMainInnerDom = function(thatBlock) {
        var mainInnerDom = $(`<div class='vp-block-inner'></div>`);
        mainInnerDom.attr("id", `vp_block-${thatBlock.getUUID()}`);
        return mainInnerDom;
    }
 
    /** class param 생성 */
    var GenerateClassInParamList = function(thatBlock) {
        var parentClassName = thatBlock.getState(STATE_parentClassName);
        var classInParamStr = `(`;
        classInParamStr += parentClassName;
        classInParamStr += `):`;
        return classInParamStr;
    }
 
    /** def param 생성 */
    var GenerateDefInParamList = function(thatBlock) {
         /** 함수 파라미터 */
         var defInParamList = thatBlock.getState(STATE_defInParamList);
         var defReturnTypeState = thatBlock.getState(STATE_defReturnType);
         var defInParamStr = `(`;
         defInParamList.forEach(( defInParam, index ) => {
             const { arg3, arg4, arg5 ,arg6 } = defInParam;
            //  if (arg3 !== '' ) {
                 
                 if (arg6 == '*args') {
                     defInParamStr += '*';
                 } else if (arg6 == '**kwargs') {
                     defInParamStr += '**';
                 }
 
                 defInParamStr += arg3;
 
                 if (arg4 == DEF_BLOCK_ARG4_TYPE.NONE || arg4 == STR_NULL) {
                    defInParamStr += '';
                 } else {
                   
                    if (arg4 != DEF_BLOCK_ARG4_TYPE.INPUT_STR) {
                        defInParamStr += ':';
                        defInParamStr += arg4;
                    } 
                    // else {
                    //     defInParamStr += ':';
                    //     defInParamStr += arg4;
                    // }
                 }
 
                 if (arg5 !== '') {
                     defInParamStr += `=${arg5}`;
                 }
 
                 for (var i = index + 1; i < defInParamList.length; i++) {
                     if (defInParamList[i].arg3 !== '') {
                         defInParamStr += `, `;
                         break;
                     }
                 };
            //  }
         });
         defInParamStr += `)`;

         if (defReturnTypeState == DEF_BLOCK_ARG4_TYPE.NONE || defReturnTypeState == STR_NULL) {
            defInParamStr += `:`;
         } else {
            if (defReturnTypeState != DEF_BLOCK_ARG4_TYPE.INPUT_STR) {
                defInParamStr += ` `;
                defInParamStr += `->`;
                defInParamStr += ` `;
                defInParamStr += defReturnTypeState;
                defInParamStr += `:`;
            } 
            // else {

            // }

         }
 
         return defInParamStr;
    }
 
    /** return param 생성 */
    var GenerateReturnOutParamList = function(thatBlock) {
        var returnOutParamList = thatBlock.getState(STATE_returnOutParamList);
        var returnOutParamStr = ` `;
        returnOutParamList.forEach(( returnInParam, index ) => {
            if (returnInParam !== '' ) {
                returnOutParamStr += `${returnInParam}`;
                for (var i = index + 1; i < returnOutParamList.length; i++) {
                    if (returnOutParamList[i] !== '') {
                        returnOutParamStr += `, `;
                        break;
                    }
                };
            }
        });
        returnOutParamStr += ``;
        return returnOutParamStr;
    }
 
    /** if param 생성 */
    var GenerateIfConditionList = function(thatBlock, blockCodeLineType) {
         var ifConditionList;
         if (blockCodeLineType == BLOCK_CODELINE_TYPE.IF) {
             ifConditionList = thatBlock.getState(STATE_ifConditionList);
         } else {
             ifConditionList = thatBlock.getState(STATE_elifConditionList);
         }
 
         var ifConditionListStr = ``;
         ifConditionList.forEach(( ifCondition, index ) => {
             const { conditionType } = ifCondition;
             if (conditionType == IF_BLOCK_CONDITION_TYPE.ARG) {
                 const { arg1, arg2, arg3, arg4, arg5, arg6 } = ifCondition;
                //  if (arg1 == '' && arg2 == '' && arg3 == ''&& (arg4 == 'none' || arg4 == '')) {
                //      return;
                //  }
                if ( !(arg1 == '' && (arg2 == 'none' || arg2 == '') && arg3 == '')) {
                    ifConditionListStr += `(`;
                }
                //  ifConditionListStr += `(`;
                 ifConditionListStr += arg1;
  
                 if ( arg2 !== 'none' ) {
                    ifConditionListStr += arg2;
                 }
                 ifConditionListStr += arg3;
         
                 if ( arg4 !== 'none' ) {
                     ifConditionListStr += arg4;
                     ifConditionListStr += arg5;
                 }
                 
                 if ( !(arg1 == '' && (arg2 == 'none' || arg2 == '') && arg3 == '')) {
                    ifConditionListStr += `)`;
                }
         
                 if ( ifConditionList.length -1 !== index ) {
                     ifConditionListStr += '';
                     ifConditionListStr += arg6;
                     ifConditionListStr += '';
                 }
             } else {
                 const { codeLine, arg6 } = ifCondition;
                 if (codeLine == '') {
                     return;
                 }
                 ifConditionListStr += `(`;
                 ifConditionListStr += codeLine;
                 ifConditionListStr += `)`;
 
                 if ( ifConditionList.length -1 !== index ) {
                     ifConditionListStr += '';
                     ifConditionListStr += arg6;
                     ifConditionListStr += '';
                 }
             }
 
         });
 
        return ifConditionListStr;
     }
 
      /** if param 생성 */
    var GenerateWhileConditionList = function(thatBlock) {
        var ifConditionList = thatBlock.getState(STATE_whileConditionList);
 

        var ifConditionListStr = ``;
        ifConditionList.forEach(( ifCondition, index ) => {
            // const { conditionType } = ifCondition;
            // if (conditionType == IF_BLOCK_CONDITION_TYPE.ARG) {
                const { arg1, arg2, arg3, arg4, arg5, arg6 } = ifCondition;
               //  if (arg1 == '' && arg2 == '' && arg3 == ''&& (arg4 == 'none' || arg4 == '')) {
               //      return;
               //  }
               if ( !(arg1 == '' && (arg2 == 'none' || arg2 == '') && arg3 == '')) {
                   ifConditionListStr += `(`;
               }
               //  ifConditionListStr += `(`;
                ifConditionListStr += arg1;
 
                if ( arg2 !== 'none' ) {
                   ifConditionListStr += arg2;
                }
                ifConditionListStr += arg3;
        
                if ( arg4 !== 'none' ) {
                    ifConditionListStr += arg4;
                    ifConditionListStr += arg5;
                }
                
                if ( !(arg1 == '' && (arg2 == 'none' || arg2 == '') && arg3 == '')) {
                   ifConditionListStr += `)`;
               }
        
                if ( ifConditionList.length -1 !== index ) {
                    ifConditionListStr += '';
                    ifConditionListStr += arg6;
                    ifConditionListStr += '';
                }
            // } else {
                // const { codeLine, arg6 } = ifCondition;
                // if (codeLine == '') {
                //     return;
                // }
                // ifConditionListStr += `(`;
                // ifConditionListStr += codeLine;
                // ifConditionListStr += `)`;

                // if ( ifConditionList.length -1 !== index ) {
                //     ifConditionListStr += '';
                //     ifConditionListStr += arg6;
                //     ifConditionListStr += '';
                // }
            // }

        });

       return ifConditionListStr;
    }
     var GenerateExceptConditionList = function(thatBlock) {
         var exceptConditionList = thatBlock.getState(STATE_exceptConditionList);
 
         var exceptConditionListStr = ``;
         exceptConditionList.forEach(( exceptCondition, index ) => {
            const { conditionType } = exceptCondition;
            if (conditionType == IF_BLOCK_CONDITION_TYPE.ARG) {
                const { arg1, arg2, arg3 } = exceptCondition;
        
                exceptConditionListStr += arg1;

                if ( arg2 == 'none' || arg2 == STR_NULL ) {
                } else {
                    exceptConditionListStr += ' ';
                    exceptConditionListStr += arg2;
                    exceptConditionListStr += ' ';
                    exceptConditionListStr += arg3;
                }
        
            } else {
                const { codeLine } = exceptCondition;
                if (codeLine == '') {
                    return;
                }
             
                exceptConditionListStr += codeLine;
            }
     
         });
 
        return exceptConditionListStr;
     }
 
     /** for param 생성 */
     var GenerateForParam = function(thatBlock) {
         var forParam = thatBlock.getState(STATE_forParam);
         const { arg1, arg2, arg3, arg4, arg5, arg6, arg7 } = forParam;
 
         var forParamStr = ``;
 
         if (arg1 !== STR_NULL) {
             forParamStr += arg1;
             forParamStr += ' ';
         }
 
         if (arg3 == FOR_BLOCK_ARG3_TYPE.ENUMERATE && arg1 !== STR_NULL && arg4 !== STR_NULL) { 
             forParamStr += ',';
         }
 
         if (arg3 == FOR_BLOCK_ARG3_TYPE.ENUMERATE && arg4 !== STR_NULL) {
             forParamStr += arg4;
             forParamStr += ' ';
         }
 
         forParamStr += 'in';
         forParamStr += ' ';
 
         if (arg3 == FOR_BLOCK_ARG3_TYPE.ZIP) {
             forParamStr += arg3;
             forParamStr += '(';
             forParamStr += arg2;
 
             if (arg7 !== '') {
                 forParamStr += ',';
                 forParamStr += ' ';
                 forParamStr += arg7;
             }
 
             forParamStr += ')';
 
         } else if (arg3 ==  FOR_BLOCK_ARG3_TYPE.ENUMERATE ) {
             forParamStr += arg3;
             forParamStr += '(';
             forParamStr += arg2;
             forParamStr += ')';
 
         } else if (arg3 ==  FOR_BLOCK_ARG3_TYPE.RANGE ) {
             forParamStr += arg3;
             forParamStr += '(';
 
             if (arg5 !== '') {
                 forParamStr += arg5;
             }
 
             if (arg5 !== '' && arg2 !== '') { 
                 forParamStr += ',';
             }
 
             if (arg2 !== '') {
                 forParamStr += ' ';
                 forParamStr += arg2;
             }
 
             if ((arg5 !== '' || arg2 !== '') && arg6 !== '') { 
                 forParamStr += ',';
             }
 
             if (arg6 !== '') {
                 forParamStr += ' ';
                 forParamStr += arg6;
             }
   
             forParamStr += ')';
 
         } else {
            if (arg3 != FOR_BLOCK_ARG3_TYPE.INPUT_STR) {
                forParamStr += arg3;
            } 

            if (arg2 != '') {
                if (arg3 == '' || arg3 == FOR_BLOCK_ARG3_TYPE.INPUT_STR) {
                    forParamStr += arg2;
                } else {
                    forParamStr += '(';
                    forParamStr += arg2;
                    forParamStr += ')';
                }
            }

         }

         return forParamStr;
     }
 
     /** Listfor param 생성 */
     var GenerateListforConditionList = function(thatBlock) {
         var listforStr = '';
         var listforReturnVar = thatBlock.getState(STATE_listforReturnVar);
         var listforPrevExpression = thatBlock.getState(STATE_listforPrevExpression);
 
         if (listforReturnVar != '') {
             listforStr += listforReturnVar;
             listforStr += ' ';
             listforStr += '=';
             listforStr += ' ';
         }
 
         listforStr += '[';
         listforStr += listforPrevExpression;
 
 
         var listforConditionList = thatBlock.getState(STATE_listforConditionList);
         listforConditionList.forEach(listforCondition => {
            //  console.log('listforCondition',listforCondition);
             const { arg1, arg2, arg3, arg4, arg5, arg6, arg7
                     , arg10, arg11, arg12, arg13, arg14, arg15  } = listforCondition;
 
             listforStr += ' ';
             listforStr += 'for';
             listforStr += ' ';
             if (arg1 !== '') {
                 listforStr += arg1;
                 listforStr += ' ';
             }
     
             if (arg3 == 'enumerate' && arg1 !== '' && arg4 !== '') { 
                 listforStr += ',';
             }
     
             if (arg3 == 'enumerate' && arg4 !== '') {
                 listforStr += arg4;
                 listforStr += ' ';
             }
     
             listforStr += 'in';
             listforStr += ' ';
     
             if (arg3 == 'zip') {
                 listforStr += arg3;
                 listforStr += '(';
                 listforStr += arg2;
     
                 if (arg7 !== '') {
                     listforStr += ',';
                     listforStr += ' ';
                     listforStr += arg7;
                 }
     
                 listforStr += ')';
     
             } else if (arg3 == 'enumerate') {
                 listforStr += arg3;
                 listforStr += '(';
                 listforStr += arg2;
                 listforStr += ')';
     
             } else if (arg3 == 'range') {
                 listforStr += arg3;
                 listforStr += '(';
     
                 if (arg5 !== '') {
                     listforStr += arg5;
                 }
     
                 if (arg5 !== '' && arg2 !== '') { 
                     listforStr += ',';
                 }
     
                 if (arg2 !== '') {
                     listforStr += ' ';
                     listforStr += arg2;
                 }
     
                 if ((arg5 !== '' || arg2 !== '') && arg6 !== '') { 
                     listforStr += ',';
                 }
     
                 if (arg6 !== '') {
                     listforStr += ' ';
                     listforStr += arg6;
                 }
       
                 listforStr += ')';
     
             } 

            else {
                if (arg3 != FOR_BLOCK_ARG3_TYPE.INPUT_STR) {
                    listforStr += arg3;
                } 
    
                if (arg2 != '') {
                    if (arg3 == '' || arg3 == FOR_BLOCK_ARG3_TYPE.INPUT_STR) {
                        listforStr += arg2;
                    } else {
                        listforStr += '(';
                        listforStr += arg2;
                        listforStr += ')';
                    }
                }
    
             }
 
             if (arg10 == 'if') {
                 listforStr += ' ';
                 listforStr += 'if';
                 listforStr += ' ';
                 listforStr += `(`;
         
                 listforStr += arg11;
                 listforStr += arg12;
                 listforStr += arg13;
         
                 if ( arg14 !== 'none' ) {
                     listforStr += arg14;
                     listforStr += arg15;
                 }
                 
                 listforStr += ' ';
                 listforStr += `)`;
                 listforStr += '';
     
             } else if (arg10 == 'inputStr') {
 
             }
         });
 
         listforStr += ']';
         return listforStr;
     }
 
     var GenerateLambdaParamList = function(thatBlock) {
         var lambdaParamStr = STR_NULL;
         var lambdaArg1State = thatBlock.getState(STATE_lambdaArg1);
         var lambdaArg2ListState = thatBlock.getState(STATE_lambdaArg2List);
         var lambdaArg2m_ListState = thatBlock.getState(STATE_lambdaArg2m_List);
         var lambdaArg3State = thatBlock.getState(STATE_lambdaArg3);
         var lambdaArg4ListState = thatBlock.getState(STATE_lambdaArg4List);
         if (lambdaArg1State != '') {
             lambdaParamStr += lambdaArg1State;
             lambdaParamStr += ' ';
             lambdaParamStr += '=';
             lambdaParamStr += ' ';
         }
    
  
         lambdaArg4ListState.forEach( (lambdaArg4, index) => {
             lambdaParamStr += lambdaArg4;
             lambdaParamStr += '(';
         });
 
         lambdaParamStr += 'lambda';
         lambdaParamStr += ' ';
         lambdaArg2ListState.forEach( (lambdaArg2, index) => {
             lambdaParamStr += lambdaArg2;
             if ( lambdaArg2ListState.length - 1 != index) {
                 if (lambdaArg2 != '') {
                    lambdaParamStr += ' ';
                    lambdaParamStr += ',';
                 }
             }
         });
   
         lambdaParamStr += ':';
       
         lambdaParamStr += MapNewLineStrToSpacebar(lambdaArg3State);
     
         lambdaParamStr += ',';
         lambdaArg2m_ListState.forEach( (lambdaArg2_m, index) => {
             lambdaParamStr += lambdaArg2_m;
             if ( lambdaArg2m_ListState.length - 1 != index) {
                //  lambdaParamStr += ' ';
                //  lambdaParamStr += ',';
                if (lambdaArg2_m != '') {
                    lambdaParamStr += ' ';
                    lambdaParamStr += ',';
                 }
             }
         });
         lambdaArg4ListState.forEach( (lambdaArg4, index) => {
             lambdaParamStr += ')';
         });
   
         return lambdaParamStr;
     }

     var GenerateImportList = function(thisBlock, indentString = STR_NULL) {
        var codeLine = STR_NULL;
        var blockName = 'import';
        var baseImportList = thisBlock.getState(STATE_baseImportList).filter(baseImport => {
            if ( baseImport.isImport == true) {
                return true;
            } else {
                return false;
            }
        });
        var customImportList = thisBlock.getState(STATE_customImportList).filter(customImport => {
            if ( customImport.isImport == true) {
                return true;
            } else {
                return false;
            }
        });

        var lineNum = 0;
        baseImportList.forEach((baseImport) => {
  
            if (lineNum > 0) {
                codeLine += indentString;
            } 
      
            codeLine += `${blockName.toLowerCase()} ${baseImport.baseImportName} as ${baseImport.baseAcronyms}`;
            if (baseImport.baseImportName == 'matplotlib.pyplot') {
                codeLine += STR_KEYWORD_NEW_LINE;
                codeLine += indentString;
                codeLine += `%matplotlib inline`;
            }

            codeLine += STR_KEYWORD_NEW_LINE;

            lineNum++;
        });

        customImportList.forEach((customImport,index ) => {
            if (lineNum > 0) {
                codeLine += indentString;
            } 

            codeLine += `${blockName.toLowerCase()} ${customImport.baseImportName} as ${customImport.baseAcronyms}`;
            if (customImport.baseImportName == 'matplotlib.pyplot') {
                codeLine += STR_KEYWORD_NEW_LINE;
                codeLine += indentString;
                codeLine += `%matplotlib inline`;
            }

            if (index != customImportList.length - 1) {
                codeLine += STR_KEYWORD_NEW_LINE;
            }

            lineNum++;
        });
        return codeLine;
     };

     var GenerateWhileBlockCode = function(thisBlock) {
        var whileBlockCode = STR_NULL;
        var whileArgsState = thisBlock.getState(STATE_whileArgs)
        var whileBlockOptionType = thisBlock.getState(STATE_whileBlockOptionType);
        const { arg1, arg2, arg3, arg4, arg5 } = whileArgsState;

        if (whileBlockOptionType == WHILE_BLOCK_TYPE.CONDITION) {
            whileBlockCode += arg4;
            whileBlockCode += arg2;
            whileBlockCode += arg3;
        } else if (whileBlockOptionType == WHILE_BLOCK_TYPE.TRUE_FALSE) {
            whileBlockCode += arg1;
        } else {
            whileBlockCode += arg1;
        }
        return whileBlockCode;
     }

     var ShowImportListAtBlock = function(thisBlock) {
        var codeLine = STR_NULL;
        // var blockName = 'import';
        var baseImportList = thisBlock.getState(STATE_baseImportList).filter(baseImport => {
            if ( baseImport.isImport == true) {
                return true;
            } else {
                return false;
            }
        });
        var customImportList = thisBlock.getState(STATE_customImportList).filter(customImport => {
            if ( customImport.isImport == true) {
                return true;
            } else {
                return false;
            }
        });

        if (baseImportList.length != 0) {
            codeLine += baseImportList[0].baseImportName + ' as ' + baseImportList[0].baseAcronyms;
        } else if (customImportList.length != 0) {
            codeLine += customImportList[0].baseImportName + ' as ' + customImportList[0].baseAcronyms;
        }
        return codeLine;
    }
    
    /**  멀티라인의 첫번째 줄만 보여준다 */
    var ShowCodeBlockCode = function(thisBlock) {
        var codeLine = thisBlock.getState(STATE_customCodeLine);
        var firstNewLine_index = codeLine.indexOf('\n');
        if (firstNewLine_index != -1) {
            var sliced_codeline = codeLine.slice(0, firstNewLine_index);
            return sliced_codeline;
        } else {
            return codeLine;
        }
    }
    

     /** TODO: blockCodeLine type에 따라 css를 다르게 해야 함 */
    var RenderBlockMainHeaderDom = function(thatBlock) {

        var blockCodeLineType =  thatBlock.getBlockCodeLineType();

        /** class 이름 */
        var className = thatBlock.getState(STATE_className);
        var classInParamStr = GenerateClassInParamList(thatBlock);
 
        /** def 이름 */
        var defName = thatBlock.getState(STATE_defName);
        var defInParamStr = GenerateDefInParamList(thatBlock);
        var returnOutParamStr = GenerateReturnOutParamList(thatBlock);
        
        /** if */ 
        var ifConditionStr = GenerateIfConditionList(thatBlock, BLOCK_CODELINE_TYPE.IF);
        var elifConditionStr = GenerateIfConditionList(thatBlock, BLOCK_CODELINE_TYPE.ELIF);
    
        var forParamStr = GenerateForParam(thatBlock);
        var lambdaParamStr = GenerateLambdaParamList(thatBlock);
        var exceptParamStr = GenerateExceptConditionList(thatBlock);
        var whileBlockCode = GenerateWhileConditionList(thatBlock);
        var importListStr = ShowImportListAtBlock(thatBlock);
        var blockName = thatBlock.getBlockName();
 
        /** true면 Block이 board에서 이름이 표시되지 않는다. */
        var isBlockName = true;
        var blockSymbol = '';
        if ( IsCodeBlockType(blockCodeLineType) == true 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.LAMBDA) {
            isBlockName = false;
        }
 
        if (blockCodeLineType == BLOCK_CODELINE_TYPE.PROPERTY) {
            blockSymbol = '@';
            isBlockName = false;
        }
        if (blockCodeLineType == BLOCK_CODELINE_TYPE.COMMENT) {
            blockSymbol = '#';
            isBlockName = false;
        }
 
        var blockUUID = thatBlock.getUUID();
        var mainHeaderDom = $(`<div class='vp-block-header'>
                                ${
                                     isBlockName == true
                                         ?`<strong class='vp-apiblock-style-flex-column-center 
                                             ${thatBlock.getBlockCodeLineType() !== BLOCK_CODELINE_TYPE.HOLDER 
                                                                                 ? VP_CLASS_BLOCK_CODETYPE_NAME
                                                                                 : ''}' 
                                                 id='vp_block-${blockUUID}'
                                                 style='margin-right:30px; 
                                                         font-size:12px; 
                                                         color:#252525;
                                                         font-weight: 700;
                                                         font-family: Consolas;'>
                                             ${blockName}
                                             </strong>`
                                         : `<strong class='vp-apiblock-style-flex-column-center' 
                                             id='vp_block-${blockUUID}'
                                                 style='font-size:12px; 
                                                         color:#252525;
                                                         font-weight: 700;
                                                         font-family: Consolas;'>
                                             ${blockSymbol}
                                            </strong>`
                                }
                                <div id='vp_block-${blockUUID}' 
                                 class='vp-apiblock-codeline-ellipsis 
                                            vp-apiblock-codeline-container-box'
                                     style=''>
                                        ${
                                            blockCodeLineType == BLOCK_CODELINE_TYPE.CLASS   
                                                ? `<div id='vp_block-${blockUUID}' 
                                                         class='vp-apiblock-style-flex-row'>
                                                        <div id='vp_block-${blockUUID}'
                                                             class='vp-block-header-class-name-${blockUUID}'
                                                            style='font-size:12px;'>
                                                            ${className}
                                                        </div>
                                                        <div id='vp_block-${blockUUID}'
                                                             class='vp-block-header-param
                                                                    vp-block-header-param-${blockUUID}'
                                                            style='font-size:12px;'>
                                                            ${className.length == 0 
                                                                ? ''
                                                                : classInParamStr}
                                                        </div>
                                                    </div>`
                                                : STR_NULL
                                        }
 
                                        ${
                                            blockCodeLineType == BLOCK_CODELINE_TYPE.DEF  
                                                ? `<div id='vp_block-${blockUUID}'
                                                        class='vp-apiblock-style-flex-row'>
                                                        <div id='vp_block-${blockUUID}'
                                                             class='vp-block-header-def-name-${blockUUID}'
                                                            style='font-size:12px;'>
                                                            ${defName}
                                                        </div>
                                                        <div id='vp_block-${blockUUID}'
                                                             class='vp-block-header-param
                                                                    vp-block-header-${blockUUID}'
                                                                style='font-size:12px;'>
                                                                ${defName.length == 0 
                                                                    ? ''
                                                                    : defInParamStr}
                                                        </div>
                                                    </div>`
                                                : STR_NULL
                                        }
                                            
 
                                        ${
                                            blockCodeLineType == BLOCK_CODELINE_TYPE.IF    
                                                ? `<div id='vp_block-${blockUUID}'
                                                        class='vp-block-header-param
                                                               vp-block-header-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${ifConditionStr}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                            blockCodeLineType == BLOCK_CODELINE_TYPE.FOR   
                                                ? `<div id='vp_block-${blockUUID}'
                                                         class='vp-block-header-param
                                                               vp-block-header-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${forParamStr}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                            blockCodeLineType == BLOCK_CODELINE_TYPE.ELIF
                                                ? `<div id='vp_block-${blockUUID}'
                                                         class='vp-block-header-param
                                                               vp-block-header-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${elifConditionStr}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                             blockCodeLineType == BLOCK_CODELINE_TYPE.WHILE 
                                                 ? `<div id='vp_block-${blockUUID}'
                                                         class='vp-block-header-param
                                                                vp-block-header-${blockUUID}'
                                                         style='font-size:12px;'>
                                                         ${whileBlockCode}
                                                     </div>`
                                                 : STR_NULL
                                         }   
                                        ${
                                            blockCodeLineType == BLOCK_CODELINE_TYPE.EXCEPT
                                                ? `<div id='vp_block-${blockUUID}'
                                                         class='vp-block-header-param
                                                               vp-block-header-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${exceptParamStr}
                                                    </div>`
                                                : STR_NULL
                                        }
 
                                        ${
                                         blockCodeLineType == BLOCK_CODELINE_TYPE.BREAK  
                                         || blockCodeLineType == BLOCK_CODELINE_TYPE.CONTINUE  
                                         || blockCodeLineType == BLOCK_CODELINE_TYPE.PASS 
                                         || blockCodeLineType == BLOCK_CODELINE_TYPE.CODE  
                                         || blockCodeLineType == BLOCK_CODELINE_TYPE.COMMENT 
                                         || blockCodeLineType == BLOCK_CODELINE_TYPE.PRINT
                                                ? `<div id='vp_block-${blockUUID}'
                                                         class='vp-block-header-param
                                                                vp-block-header-${blockUUID}'
                                                        style='font-size:12px; 
                                                               color:${ShowCodeBlockCode(thatBlock) == STR_NULL 
                                                                             ? `${COLOR_GRAY_input_your_code}` 
                                                                             : ''};'>
                                                        ${ShowCodeBlockCode(thatBlock) == STR_NULL
                                                            ? STR_INPUT_YOUR_CODE
                                                            : ShowCodeBlockCode(thatBlock)}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                         blockCodeLineType == BLOCK_CODELINE_TYPE.PROPERTY   
                                                ? `<div id='vp_block-${blockUUID}'
                                                         class='vp-block-header-param
                                                                vp-block-header-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${thatBlock.getState(STATE_customCodeLine)}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                            blockCodeLineType == BLOCK_CODELINE_TYPE.RETURN        
                                                ? `<div id='vp_block-${blockUUID}'
                                                         class='vp-block-header-param
                                                               vp-block-header-${blockUUID}'
                                                         style='font-size:12px;'>
                                                        ${returnOutParamStr}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                             blockCodeLineType == BLOCK_CODELINE_TYPE.LAMBDA        
                                                 ? `<div id='vp_block-${blockUUID}'
                                                         class='vp-block-header-param
                                                                vp-block-header-${blockUUID}'
                                                         style='font-size:12px;'>
                                                         ${lambdaParamStr}
                                                     </div>`
                                                 : STR_NULL
                                         }     
                                         ${
                                             blockCodeLineType == BLOCK_CODELINE_TYPE.BLANK        
                                                 ? `<div id='vp_block-${blockUUID}'
                                                         style='background-color:transparent;'>
                                                      
                                                     </div>`
                                                 : STR_NULL
                                         }    
                                         ${
                                            blockCodeLineType == BLOCK_CODELINE_TYPE.IMPORT        
                                                ? `<div id='vp_block-${blockUUID}'
                                                        class='vp-block-header-param
                                                               vp-block-header-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${importListStr}
                                                    </div>`
                                                : STR_NULL
                                        }     
                                        </div>
                                </div>`);
         mainHeaderDom.attr("id", `vp_block-${blockUUID}`);
        return mainHeaderDom;
    }  
 
    var RenderOptionPageName = function(thatBlock, name, blockCodeLineType, uuid) {
         var classStr = STR_NULL;
         var idStr = STR_NULL;
         var inputStyleStr = STR_NULL;
         var resetButton = null;
         var blockCodeName = thatBlock.getBlockName();
         var blockContainerThis = thatBlock.getBlockContainerThis();
         var uuid = thatBlock.getUUID();
 
         if (blockCodeLineType == BLOCK_CODELINE_TYPE.CLASS) {
             idStr = `vp_apiblockClassOptionName${uuid}`;
             classStr = `vp-apiblock-input-class-name-${uuid}`;
             blockCodeName = 'Name';
             inputStyleStr = 'width: 82%';
             /** state className에 문자열이 1개도 없을 때 */
             var classNameState = thatBlock.getState(STATE_className);
             if (classNameState == STR_NULL) {
                 classStr += STR_ONE_SPACE;
                 classStr += VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED;
             }
 
         } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.DEF) {
             idStr = `vp_apiblockDefOptionName${uuid}`;
             classStr = `vp-apiblock-input-def-name-${uuid}`;
             blockCodeName = 'Name';
             inputStyleStr = 'width: 82%';
             /** state defName에 문자열이 1개도 없을 때 */
             var defNameState = thatBlock.getState(STATE_defName);
             if (defNameState == STR_NULL) {
                classStr += STR_ONE_SPACE;
                classStr += VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED;
             }
 
         } 
        
         var nameDom = $(`<div class='vp-apiblock-blockoption-block 
                                      vp-apiblock-style-flex-row-between' 
                                style='position:relative;'>
                            <span class='vp-block-optiontab-name 
                                         vp-apiblock-style-flex-column-center'>
                                ${blockCodeName}
                            </span>
                            <input id='${idStr}'
                                   class='vp-apiblock-blockoption-input ${classStr}'
                                   style='${inputStyleStr}' 
                                   value="${name}"
                                   placeholder='input code line' ></input>   
                                                                             
                        </div>`);
                        
        if (resetButton !== null) {
            $(nameDom).append(resetButton);
        }
        return nameDom;
    }
 
    var RenderInParamContainer = function(block, inParamList) {
 
        var inParamContainer = $(`<div class='vp-apiblock-ifoption-container'>
                                            <div class='vp-apiblock-tab-navigation-node-block-title'>
                                                <span class='vp-block-optiontab-name'>
                                                    param
                                                </span>
                                                <div class='vp-apiblock-style-flex-row-center' >
 
                                          
                                                </div>
                                            </div>
                                        </div>`);
        return inParamContainer;
    }
 
    var RenderBottomOptionTitle = function(title) {
        var titleDom = $(`<div class='vp-apiblock-option-container'
                               style='margin-top:5px;'>
                                <div class='vp-apiblock-tab-navigation-node-block-title'>
                                    <span class='vp-block-optiontab-name'>${title}</span>
                                    
                                </div>
                            </div>`);
        return titleDom;
    }
 
    var RenderDefaultOrDetailButton = function(thatBlock, uuid, blockCodeLineType) {
        var defaultOptionTitle = STR_NULL;
        var detailOptionTitle = STR_NULL;
        if (blockCodeLineType == BLOCK_CODELINE_TYPE.IMPORT) {
            defaultOptionTitle = `Default Import`;
            detailOptionTitle = `Custom Import`;
        } else {
            defaultOptionTitle = `Default Option`;
            detailOptionTitle = `Detail Option`; 
        }
 
        var isBaseImportPage = thatBlock.getState('isBaseImportPage');
        var defaultOrDetailButton = $(`<div class='vp-apiblock-style-flex-row-between'
                                            style='margin-top:5px;'>
 
                                            <button class='vp-apiblock-default-option-${uuid} 
                                                           vp-apiblock-default-detail-option-btn
                                                           ${isBaseImportPage == true ? 
                                                                'vp-apiblock-option-btn-selected': 
                                                                ''}'>
                                                    ${defaultOptionTitle}
                                            </button>
 
                                            <button class='vp-apiblock-detail-option-${uuid} 
                                                           vp-apiblock-default-detail-option-btn
                                                           ${isBaseImportPage == false 
                                                                ? 'vp-apiblock-option-btn-selected': 
                                                                ''}'>
                                                    ${detailOptionTitle}
                                            </button>
                                        </div>`);
        return defaultOrDetailButton;
    }
 
    /** 특정 input태그 값 입력 안 될시 빨간색 border 
     *  값 입력 x -> font-weight 300
     *  값 입력 o -> font-weight 700
     */
    var RenderInputRequiredColor = function(thatBlock) {
        if ($(thatBlock).val() == STR_NULL) {
            // $(thatBlock).css(STR_FONT_WEIGHT, NUM_FONT_WEIGHT_300);
            $(thatBlock).addClass(VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED)
        } else {
            // $(thatBlock).css(STR_FONT_WEIGHT, NUM_FONT_WEIGHT_700);
            $(thatBlock).removeClass(VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED); 
        }
    }
 
    var RenderSelectRequiredColor = function(target, selectedValue) {
        if (selectedValue == STR_NULL) {
            // $(thatBlock).css(STR_FONT_WEIGHT, NUM_FONT_WEIGHT_300);
            $(target).addClass(VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED)
        } else {
            // $(thatBlock).css(STR_FONT_WEIGHT, NUM_FONT_WEIGHT_700);
            $(target).removeClass(VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED); 
        }
    }

 
    var RenderCustomImportDom = function(customImportData, index) {
        const { isImport, baseImportName, baseAcronyms } = customImportData;
        var customImportDom = $(`<div class='vp-apiblock-style-flex-row-between'
                                      style='margin-top:5px;'>
 
                                    <div class='vp-apiblock-style-flex-column-center'>
                                        <label class='vp-apiblock-style-flex-column-center'>
                                            <input class='vp-apiblock-blockoption-custom-import-input
                                                        vp-apiblock-blockoption-custom-import-input-${index}' 
                                                
                                                type='checkbox' 
                                                ${isImport == true ? STR_CHECKED: ''}>
                                            </input>
                                            <span style='margin-top: -7px;'>
                                            </span>
                                        </label>
                                    </div>
 
                                    <select class='vp-apiblock-select
                                                    vp-apiblock-blockoption-custom-import-select
                                                    vp-apiblock-blockoption-custom-import-select-${index}'
                                            style='margin-right:5px;'>
                                        <option value='numpy' ${baseImportName == 'numpy' ? STR_SELECTED : ''}>
                                            numpy
                                        </option>
                                        <option value='pandas' ${baseImportName == 'pandas' ? STR_SELECTED : ''}>
                                            pandas
                                        </option>
                                        <option value='matplotlib' ${baseImportName == 'matplotlib' ? STR_SELECTED : ''}>
                                            matplotlib
                                        </option>
                                        <option value='seaborn' ${baseImportName == 'seaborn' ? STR_SELECTED : ''}>
                                            seaborn
                                        </option>
                                        <option value='os' ${baseImportName == 'os' ? STR_SELECTED : ''}>
                                            os
                                        </option>
                                        <option value='sys' ${baseImportName == 'sys' ? STR_SELECTED : ''}>
                                            sys
                                        </option>
                                        <option value='time' ${baseImportName == 'time' ? STR_SELECTED : ''}>
                                            time
                                        </option>
                                        <option value='datetime' ${baseImportName == 'datetime' ? STR_SELECTED : ''}>
                                            datetime
                                        </option>
                                        <option value='random' ${baseImportName == 'random' ? STR_SELECTED : ''}>
                                            random
                                        </option>
                                        <option value='math' ${baseImportName == 'math' ? STR_SELECTED : ''}>
                                            math
                                        </option>
                                    </select>
 
                                    <div class='vp-apiblock-style-flex-column-center'>
                                        <input class='vp-apiblock-blockoption-custom-import-textinput
                                                      vp-apiblock-blockoption-custom-import-textinput-${index}
                                                    ${baseAcronyms == '' 
                                                        ? 'vp-apiblock-option-input-required' 
                                                        : ''}'
                                                style='width: 90%;' 
                                                type='text' 
                                                placeholder='input import'
                                                value='${baseAcronyms}'></input>
                                    </div>
 
                                </div>`);
        return customImportDom;
    }
 
    var RenderDefaultOrCustomImportContainer = function(importType, countisImport) {
        var name = STR_NULL;
        var customImportButton = STR_NULL;
        if (importType == IMPORT_BLOCK_TYPE.DEFAULT) {
            name = STR_DEFAULT;
        } else {
            name = STR_CUSTOM;
            customImportButton = MakeOptionPlusButton('', ' + import', 'vp-apiblock-custom-import-plus-btn');
            customImportButton = customImportButton.toString();
        }
    
        var container = $(`<div class='vp-apiblock-blockoption-${name}-import-container'>
                                <div class='vp-apiblock-tab-navigation-node-block-title'>
                                    <span class='vp-block-optiontab-name
                                                 vp-apiblock-style-flex-column-center'>${name}</span>
                                    <div class='vp-apiblock-style-flex-row-center'>
                                        <span class='vp-apiblock-${name}-import-number
                                                     vp-apiblock-style-flex-column-center'
                                                style='margin-right:5px;'>
                                                ${countisImport} Selected
                                        </span>
                                            ${customImportButton}
                                       
                                    </div>
                                </div>
                            </div>`);
 
        return container;
    }
 
    var RenderDefaultImportDom = function(baseImportData, index) {
        const { isImport, baseImportName, baseAcronyms } = baseImportData;
        var defaultImportDom = $(`<div class='vp-apiblock-style-flex-row-between'
                                        style='padding: 0.1rem 0;
                                               margin-top:5px;'>
                                        <div class='vp-apiblock-style-flex-column-center'>
                                            <label class='vp-apiblock-style-flex-column-center'>
                                                <input class='vp-apiblock-blockoption-default-import-input-${index}'
                                                        type='checkbox'
                                                        ${isImport == true 
                                                            ? 'checked'
                                                            : ''}>
                                                </input>             
                                                <span style='margin-top: -7px;'>
                                                </span>
                                            </label>
         
                                        </div>
                                        <div class='vp-apiblock-style-flex-column-center'>
                                            <span style='font-size:12px; font-weight:700;'> ${baseImportName}</span>
                                        </div>
                                        <div class='vp-apiblock-style-flex-column-center'
                                            style='width: 50%;     text-align: center;'>
                                            <span class=''>${baseAcronyms}</span>
                                
                                        </div>
                                </div>`);
        return defaultImportDom;
    }
 
    var RenderRunBlockButton = function() {
        var runBtn = $(`<div class='vp-block-option-btn
                                       vp-apiblock-style-flex-column-center'>
                                <i class="vp-fa fa fa-play vp-block-option-icon"></i>
                            </div>`);
        return runBtn;                     
    }
 
    var RenderDeleteBlockButton = function() {
        var deleteBtn = $(`<div class='vp-block-delete-btn
                                       vp-apiblock-style-flex-column-center'>
                                <i class="vp-fa fa fa-times vp-block-option-icon"></i>
                            </div>`);
        return deleteBtn;                     
    }
 
    var RenderFocusedPage = function(focusedPageType) {
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BUTTONS)).css(STR_BORDER, STR_TRANSPARENT);
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BUTTONS)).css(STR_BORDER_RIGHT, `1px ${STR_SOLID} #d4d4d4`);
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BUTTONS)).css(STR_BORDER_TOP_LEFT_RADIUS, '7px');
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BUTTONS)).css(STR_BORDER_BOTTOM_LEFT_RADIUS, '7px');
 
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).css(STR_BORDER, STR_TRANSPARENT);
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).css(STR_BORDER_RIGHT, `1px ${STR_SOLID} #d4d4d4`);
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).css(STR_BORDER_TOP_RIGHT_RADIUS, '7px');
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).css(STR_BORDER_BOTTOM_RIGHT_RADIUS, '7px');

        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_BORDER, STR_TRANSPARENT);
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_BORDER_TOP_RIGHT_RADIUS, '7px');
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_BORDER_BOTTOM_RIGHT_RADIUS, '7px');
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css('border-left', '1px solid #d4d4d4');
 
        if ( focusedPageType == FOCUSED_PAGE_TYPE.BUTTONS ) {
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BUTTONS)).css(STR_BORDER, `${STR_3PX} ${COLOR_FOCUSED_PAGE} ${STR_SOLID}`);
        } else if (focusedPageType == FOCUSED_PAGE_TYPE.EDITOR) {
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).css(STR_BORDER, `${STR_3PX} ${COLOR_FOCUSED_PAGE} ${STR_SOLID}`);
        } else if (focusedPageType == FOCUSED_PAGE_TYPE.OPTION) {
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_BORDER, `${STR_3PX} ${COLOR_FOCUSED_PAGE} ${STR_SOLID}`);
        } else {
 
        }
    }
 
    var RenderOptionTitle = function(thatBlock) {
        var blockCodeLineName = thatBlock.getBlockName();
        blockCodeLineName = blockCodeLineName.charAt(0).toUpperCase() + blockCodeLineName.slice(1)
        var optionTitle = $(`<div class='vp-apiblock-tab-navigation-node-childs-option-title
                                         vp-accordion-header'>
                                <div class='vp-apiblock-panel-area-vertical-btn
                                            vp-apiblock-panel-area-vertical-btn-${thatBlock.getUUID()}
                                            vp-apiblock-arrow-up'>▼</div>
                                    <span class='vp-block-blocktab-name 
                                                    vp-block-blocktab-name-title
                                                    vp-accordion-caption'
                                            style="font-size: 16px;">${blockCodeLineName} Option</span>
                                
                           </div>`);
 
         /** FIXME: 임시코드 추후 삭제 */
         $(document).off(STR_CLICK, `.vp-apiblock-panel-area-vertical-btn-${thatBlock.getUUID()}`);
         $(document).on(STR_CLICK, `.vp-apiblock-panel-area-vertical-btn-${thatBlock.getUUID()}`, function() {
                 if ($(this).hasClass(`vp-apiblock-arrow-down`)) {
                     $(this).removeClass(`vp-apiblock-arrow-down`);
                     $(this).addClass(`vp-apiblock-arrow-up`);
                     $(this).html(`▼`);
                     $(this).parent().next().removeClass(`vp-apiblock-minimize-10px`);
                 } else {
                     $(this).removeClass(`vp-apiblock-arrow-up`);
                     $(this).addClass(`vp-apiblock-arrow-down`);
                     $(this).html(`▶`);
                     $(this).parent().next().addClass(`vp-apiblock-minimize-10px`);
                 }
         });
        return optionTitle;
    }
 
    var RenderPropertyDom = function(thatBlock) {
        var uuid = thatBlock.getUUID();
        var blockContainerThis = thatBlock.getBlockContainerThis();
        var propertyCodeLineState = thatBlock.getState(STATE_customCodeLine);
 
        var propertyDom = $(`<div class='vp-block-blockoption 
                                         vp-apiblock-blockoption-block 
                                         vp-apiblock-blockoption-inner 
                                         vp-apiblock-style-flex-row-between' 
                                  style='position: relative;'>
                    
                                <span class='vp-apiblock-style-flex-column-center'
                                      style='margin-right: 5px;'>
                                    @
                                </span>                                     
                            </div>`);
 
        var inputDom = $(`<input class='vp-apiblock-blockoption-input'
                                 id='vp_apiblockCodeOptionInput${uuid}'
                                style='width: 85%; 
                                       margin-right: 5px;' 
                                value="${propertyCodeLineState}"
                                placeholder='input property' >
                            </input> `);
 
        var resetButton = $(`<button class='vp-apiblock-option-reset-button 
                                            vp-block-btn'>
                                Reset
                             </button>`);
 
        $(resetButton).click(function() {                                    
            thatBlock.setState({
                customCodeLine: STR_NULL
            });
            $(`#vp_apiblockCodeOptionInput${uuid}`).html(STR_NULL);
            $(`.vp-block-header-${thatBlock.getUUID()}`).html(thatBlock.getState(STATE_customCodeLine));
            blockContainerThis.renderBlockOptionTab();
            blockContainerThis.bindCodeBlockInputFocus(thatBlock);
        });
 
        propertyDom.append(inputDom);
        propertyDom.append(resetButton);
        return propertyDom;                                        
    };

 
    var RenderClassParentDom = function(thatBlock) {
        var uuid = thatBlock.getUUID();
        var parentClassName = thatBlock.getState(STATE_parentClassName);
 
        var name = 'Inheritance';
        var classStr = `vp-apiblock-input-param-${0}-${uuid}`;
        var inputStyleStr = 'width:66%;';
 
 
        var nameDom = $(`<div class='vp-block-blockoption 
                                        vp-apiblock-blockoption-block 
                                        vp-apiblock-blockoption-inner 
                                        vp-apiblock-style-flex-row-between' 
                                style='position:relative;'>
                                <span class='vp-block-optiontab-name 
                                             vp-apiblock-style-flex-column-center'>${name}</span>
                                <input class='vp-apiblock-blockoption-input 
                                              ${classStr}'
                                    style='${inputStyleStr}' 
                                    value="${parentClassName}"
                                    placeholder='input parent class' ></input>   
                                                                                
                                </div>`);
        return nameDom;
    }
 
    /**
     * @param {string} inputValue 
     */
    var RenderCodeBlockInputRequired = function(thisBlock, inputValue, state) {
        /** 어떤 데이터도 입력되지 않을 때 */
        // var thisBlock = this;
        if (inputValue == STR_NULL) {
            $(`.vp-block-header-${thisBlock.getUUID()}`).html(STR_INPUT_YOUR_CODE);
            $(`.vp-block-header-${thisBlock.getUUID()}`).css(STR_COLOR, COLOR_GRAY_input_your_code);
            return;
        }
 
        /** 데이터가 입력되었을 때 */
        $(`.vp-block-header-${thisBlock.getUUID()}`).html(state);
        $(`.vp-block-header-${thisBlock.getUUID()}`).css(STR_COLOR, COLOR_BLACK);
    }
 
     var RenderHTMLDomColor = function(block, htmlDom) {
         var blockCodeLineType = block.getBlockCodeLineType()
 
         /** class & def 블럭 */
         if ( blockCodeLineType == BLOCK_CODELINE_TYPE.CLASS 
             || blockCodeLineType == BLOCK_CODELINE_TYPE.DEF) {
             $(htmlDom).addClass(VP_BLOCK_BLOCKCODELINETYPE_CLASS_DEF);
             
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
             || blockCodeLineType == BLOCK_CODELINE_TYPE.IMPORT
             || blockCodeLineType == BLOCK_CODELINE_TYPE.LAMBDA
             || blockCodeLineType == BLOCK_CODELINE_TYPE.PROPERTY ) {
                 
             //  COLOR_CONTROL;
             $(htmlDom).addClass(VP_BLOCK_BLOCKCODELINETYPE_CONTROL);
 
         } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.BLANK){
             $(htmlDom).css('background-color', 'transparent !important');
    
         } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.HOLDER ) {

         } else {
             $(htmlDom).addClass(VP_BLOCK_BLOCKCODELINETYPE_CODE);
         }
         return htmlDom;
     }
 
     /** FIXME: 추후 제거
      * buttons와 option page의 arrow 조작
      */
     var BindArrowBtnEvent = function() {
         /**  블럭 up down 버튼 */
         $(`.vp-apiblock-panel-area-vertical-btn`).off();
         $(`.vp-apiblock-panel-area-vertical-btn`).click(function() {
             if ($(this).hasClass(`vp-apiblock-arrow-down`)) {
                 $(this).removeClass(`vp-apiblock-arrow-down`);
                 $(this).addClass(`vp-apiblock-arrow-up`);
                 $(this).html(`▼`);
                 $(this).parent().parent().removeClass(`vp-apiblock-minimize`);
             } else {
                 $(this).removeClass(`vp-apiblock-arrow-up`);
                 $(this).addClass(`vp-apiblock-arrow-down`);
                 $(this).html(`▶`);
                 $(this).parent().parent().addClass(`vp-apiblock-minimize`);
             }
         });
     }
    return {
        RenderBlockMainDom
        , RenderBlockLeftHolderDom
        , RenderBlockMainInnerDom
        , RenderBlockMainHeaderDom
        , RenderDefaultImportDom
        , RenderCustomImportDom 

        , RenderDefaultOrCustomImportContainer

        , RenderInParamContainer
     
        , RenderOptionPageName

        , RenderBottomOptionTitle
 
        , RenderDefaultOrDetailButton
 
        , RenderRunBlockButton
        , RenderDeleteBlockButton
        , RenderFocusedPage
 
        , RenderInputRequiredColor
        , RenderSelectRequiredColor
        , RenderOptionTitle
        , RenderPropertyDom
 
        , RenderClassParentDom
     
        , RenderCodeBlockInputRequired
        
        , RenderHTMLDomColor
 
        , GenerateClassInParamList
        , GenerateDefInParamList
        , GenerateReturnOutParamList
        , GenerateIfConditionList
        , GenerateExceptConditionList
        , GenerateForParam
        , GenerateListforConditionList
        , GenerateLambdaParamList
        , GenerateImportList
        , GenerateWhileBlockCode
        , GenerateWhileConditionList

        , ShowImportListAtBlock
        , ShowCodeBlockCode

        , BindArrowBtnEvent
    }
 });
 