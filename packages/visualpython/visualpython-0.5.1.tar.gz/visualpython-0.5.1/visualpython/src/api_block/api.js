define([
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'

    , './config.js'
    , './constData.js'
], function ( vpCommon, vpConst, sb,
               config, constData ) {
    const { API_BLOCK_VERSION_v0_1 } = config;
    const { BLOCK_CODELINE_TYPE
            , BLOCK_DIRECTION
            , VP_CLASS_APIBLOCK_BODY 
            , VP_CLASS_PREFIX

            , STR_CLASS
            , STR_DEF
            , STR_IF
            , STR_FOR
            , STR_WHILE
            , STR_IMPORT
            , STR_API
            , STR_TRY
            , STR_EXCEPT
            , STR_FINALLY
            , STR_RETURN
            , STR_BREAK
            , STR_CONTINUE
            , STR_PASS
            , STR_PROPERTY
            , STR_CODE
            , STR_LAMBDA
            , STR_ELIF
            , STR_ELSE
            , STR_FOCUS
            , STR_BLUR
            , STR_INPUT } = constData;

    // stateApi
    /** FindStateValue 함수
    *  state를 while루프로 돌면서 돌면서 keyName과 일치하는 state의 value값을 찾아 리턴한다
    *  없으면 null을 리턴한다.
    *  @param {object} state 
    *  @param {string} keyName 
    *  @returns {any | null} returnValueOrNull
    */           
    var FindStateValue = function(state, keyName) {
        var result = [];
        var stack = [{ context: result
                    , key: 0
                        , value: state }];
        var currContext;
        var returnValueOrNull = null; 
        while (currContext = stack.pop()) {
            var { context, key, value } = currContext;

            if (!value || typeof value != 'object') {
                if (key == keyName) {
                    returnValueOrNull = value;
                    break;
                }
                
                context[key] = value; 
            }
            else if (Array.isArray(value)) {
                if (key == keyName) {
                    returnValueOrNull = value;
                    break;
                }
        
            } else {
                if (key == keyName) {
                    returnValueOrNull = value;
                    break;
                }
                context = context[key] = Object.create(null);
                Object.entries(value).forEach(([ key,value ]) => {
                    stack.push({ context, key, value });
                });
            }
        };
        return returnValueOrNull;
    };

    /** ChangeOldToNewState 함수
    *  oldState(이전 state 데이터)와 newState(새로운 state 데이터)를 비교해서
        newState로 들어온 새로운 값을 oldState에 덮어 씌운다.
    *  @param {Object} oldState 
    *  @param {Object} newState 
    *  @returns {Object}
    */
    var ChangeOldToNewState = function(oldState, newState) {
        var result = [];
        var stack = [{ context: result
                        , key: 0
                        , value: oldState }];
        var currContext;
        while (currContext = stack.pop()) {
            var { context, key, value } = currContext;

            if (!value || typeof value != 'object') {
                var newValue = FindStateValue(newState, key);
                if ( newValue == "") {
                    context[key] = "";
                }
                else if (newValue == false) {
                    context[key] = false;
                }
                else {
                    context[key] = newValue || value;
                }
            }
            else if (Array.isArray(value)) {
                var newValue = FindStateValue(newState, key);
                context[key] = newValue || value;
            } 
            else {
                context = context[key] = Object.create(null);
                Object.entries(value).forEach(([ key, value ]) => {
                    stack.push({context, key, value});
                });
            }
        };
        return result[0];
    };    
    /** CreateOneArrayValueAndGet
        *  배열의 특정 인덱스 값을 생성하고 새로운 배열을 리턴한다
        *  @param {Array} array 
        *  @param {number} index
        *  @param {number | string} newValue 
        *  @returns {Array} New array
        */
    var CreateOneArrayValueAndGet = function(array, index, newValue) {
        return [ ...array.slice(0, index+1), newValue,
                 ...array.slice(index+1, array.length) ]
    }

    /** UpdateOneArrayValueAndGet
        *  배열의 특정 인덱스 값을 업데이트하고 업데이트된 새로운 배열을 리턴한다
        *  @param {Array} array 
        *  @param {number} index
        *  @param {number | string} newValue 
        *  @returns {Array} New array
        */
    var UpdateOneArrayValueAndGet = function(array, index, newValue) {
        return [ ...array.slice(0, index), newValue,
                 ...array.slice(index+1, array.length) ]
    }

    /** DeleteOneArrayValueAndGet
    *  배열의 특정 인덱스 값을 삭제하고 삭제된 새로운 배열을 리턴한다
    *  @param {Array} array 
    *  @param {number} index 
    *  @returns {Array} New array
    */
    var DeleteOneArrayValueAndGet = function(array, index) {
        return [ ...array.slice(0, index), 
                 ...array.slice(index+1, array.length) ]
    }

    /** updateTwoArrayValueAndGet
    *  2차원 배열의 특정 인덱스 값을 업데이트하고 업데이트된 새로운 배열을 리턴한다
    *  @param {Array} array 
    *  @param {number} row
    *  @param {number} col
    *  @param {number | string} newValue 
    *  @returns {Array} New array
    */
    var updateTwoArrayValueAndGet = function(twoarray, row, col, newValue) {
        var newArray = [...twoarray[row].slice(0, col),newValue,
                        ...twoarray[row].slice(col + 1, twoarray[row].length)]
        return [ ...twoarray.slice(0, row), newArray,
                ...twoarray.slice(row+1, twoarray.length) ]
    }
    /** deleteTwoArrayValueAndGet
    *  2차원 배열의 특정 인덱스 값을 삭제하고 삭제된 새로운 배열을 리턴한다
    *  @param {Array} array 
    *  @param {number} row 
    *  @param {number} col
    *  @returns {Array} New array
    */
    var deleteTwoArrayValueAndGet = function(twoarray, row, col) {
        var newArray = [...twoarray[row].slice(0, col),
                        ...twoarray[row].slice(col + 1, twoarray[row].length)]
        return [ ...twoarray.slice(0, row), newArray,
                ...twoarray.slice(row+1, twoarray.length) ]
    }

    var MakeFirstCharToUpperCase = function(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    var MapTypeToName = function(type) {
        var name = ``;
        switch (type) {
            case BLOCK_CODELINE_TYPE.CLASS: {
                name = STR_CLASS;
                break;
            }
            case BLOCK_CODELINE_TYPE.DEF: {
                name = STR_DEF;
                break;
            }
            case BLOCK_CODELINE_TYPE.IF: {
                name = STR_IF;
                break;
            }
            case BLOCK_CODELINE_TYPE.ELIF: {
                name = STR_ELIF;
                break;
            }
            case BLOCK_CODELINE_TYPE.ELSE: {
                name = STR_ELSE;
                break;
            }
            case BLOCK_CODELINE_TYPE.FOR: {
                name = STR_FOR;
                break;
            }
            case BLOCK_CODELINE_TYPE.FOR_ELSE: {
                name = STR_ELSE;
                break;
            }
            case BLOCK_CODELINE_TYPE.WHILE: {
                name = STR_WHILE;
                break;
            }
            case BLOCK_CODELINE_TYPE.IMPORT: {
                name = STR_IMPORT;
                break;
            }
            case BLOCK_CODELINE_TYPE.API: {
                name = STR_API;
                break;
            }
            case BLOCK_CODELINE_TYPE.TRY: {
                name = STR_TRY;
                break;
            }
            case BLOCK_CODELINE_TYPE.EXCEPT: {
                name = STR_EXCEPT;
                break;
            }
            case BLOCK_CODELINE_TYPE.FINALLY: {
                name = STR_FINALLY;
                break;
            }
            case BLOCK_CODELINE_TYPE.RETURN: {
                name = STR_RETURN;
                break;
            }
            case BLOCK_CODELINE_TYPE.BREAK: {
                name = STR_BREAK;
                break;
            }
            case BLOCK_CODELINE_TYPE.CONTINUE: {
                name = STR_CONTINUE;
                break;
            }
            case BLOCK_CODELINE_TYPE.PASS: {
                name = STR_PASS;
                break;
            }
            case BLOCK_CODELINE_TYPE.PROPERTY: {
                name = STR_PROPERTY;
                break;
            }
            case BLOCK_CODELINE_TYPE.CODE: {
                name = STR_CODE;
                break;
            }
            case BLOCK_CODELINE_TYPE.LAMBDA: {
                name = STR_LAMBDA;
                break;
            }
            case BLOCK_CODELINE_TYPE.BLANK: {
                name = 'blank';
                break;
            }
            case BLOCK_CODELINE_TYPE.COMMENT: {
                name = 'comment';
                break;
            }
            case BLOCK_CODELINE_TYPE.SAMPLE: {
                name = 'sample';
                break;
            }
            case BLOCK_CODELINE_TYPE.PRINT: {
                name = 'print';
                break;
            }
            case BLOCK_CODELINE_TYPE.HOLDER: {
                name = '';
                break;
            }
            default: {
                break;
            }
        }
        return name;
    }

    var RemoveSomeBlockAndGetBlockList = function(allArray, exceptArray) {
        var lastArray = [];
        allArray.forEach((block) => {
            var is = exceptArray.some((exceptBlock) => {
                if ( block.getUUID() == exceptBlock.getUUID() ) {
                    return true;
                } 
            });

            if (is !== true) {
                lastArray.push(block);
            } 
        });
        return lastArray;
    }
    
    var DestructureFromBlockArray = function( stack, currBlockList ) {
        var tempBlockList = [];
        currBlockList.forEach(block => {
            tempBlockList.push(block);
        });
        
        /** FIXME: 추후 private 함수로 따로 분화
         *  block데이터를 배열에 담을때 INDENT 타입과 DOWN 타입의 위치 변경
         *  DOWN 앞으로 INDENT 뒤로
         */
        tempBlockList = tempBlockList.sort((block1,b) => {
            if (block1.getDirection() == BLOCK_DIRECTION.INDENT) {
                return 1;
            } else {
                return -1;
            }
        });
        tempBlockList.forEach(el => {
            stack.unshift(el);
        });  
        return stack;  
    }
   
    /** if, for 블럭 등에서 여러개 변수 중 특정 랜덤 변수를 선택할 때 사용 */
    var ShuffleArray = function(array) {
        const shuffledArray = array
                                .map(a => ([Math.random(),a]))
                                .sort((a,b) => a[0]-b[0])
                                .map(a => a[1]);
        return shuffledArray[0];
    }

    /** API BLOCK 이미지 아이콘 셀렉트 함수 */
    var GetImageUrl = function(imageFile) {
        var url = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.RESOURCE_PATH + 'api_block/' + imageFile;
        return url;
    }

    /** 100px string -> 100 number 로 바꾸는 함수
     *  @param {string} pxStr 
     */
    var PxStrToNum = function(pxStr) {
        var index = pxStr.indexOf('p');
        if (index !== -1) {
            var slicedPxStr = pxStr.slice(0,index);
            var slicedPxNum = parseFloat(slicedPxStr);
            return slicedPxNum;
        } else {
            /** 존재하면 안 되는 분기 */
            AssertError('실행 중 존재하면 안 되는 분기에 도달했습니다.');
        }
    }
    
    /** 현재 삭제 */
    var generateAPIBlockCode_v0_1 = function() {

    }
   /** 현재 삭제 */
    var GenerateAPIBlockCode = function(apiblockVersion) {
        if (apiblockVersion == API_BLOCK_VERSION_v0_1) {
            generateAPIBlockCode_v0_1();
        }
    }

    /** development -> alert
     *  production -> console.log
     */
    var AssertError = function(errorMessage) {
        console.log(errorMessage);
    }

    /** 기능 삭제 */
    var MapNewLineStrToSpacebar = function(str, indentString) {
        // return str;
        var _str = str.replace(/(\r\n\t|\n|\r\t)/gm,`\n${indentString}`);
        return _str;
    }

    /** API Block에서 자체적으로 input을 제어하기 위한 api */
    var ControlToggleInput = function() {
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BODY)).on(STR_FOCUS, STR_INPUT, function() {
            Jupyter.notebook.keyboard_manager.disable();
        });
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BODY)).on(STR_BLUR, STR_INPUT, function() {
            Jupyter.notebook.keyboard_manager.enable();
        });
    }

    /**
     * 텍스트 박스 라인 넘버 설정
     * @vpCommon_custom
     * @param {object} trigger 이벤트 트리거 객체
     */
    var SetTextareaLineNumber_apiBlock = function(trigger, textareaValue) {
        var rowCnt = textareaValue.split('\n').length;
        var sbLineText = new sb.StringBuilder();

        for (var idx = 1; idx <= rowCnt; idx++) {
            sbLineText.appendLine(idx);
        }

        $(trigger).prev(vpCommon.formatString(".{0}", vpConst.MANUAL_CODE_INPUT_AREA_LINE)).val(sbLineText.toString());
    }

    var IsCanHaveIndentBlock = function(blockCodeLineType) {
        if ( blockCodeLineType == BLOCK_CODELINE_TYPE.CLASS
            || blockCodeLineType == BLOCK_CODELINE_TYPE.DEF

            || blockCodeLineType == BLOCK_CODELINE_TYPE.IF 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR
            || blockCodeLineType == BLOCK_CODELINE_TYPE.TRY
            || blockCodeLineType == BLOCK_CODELINE_TYPE.WHILE ) {
           return true;
       } else {
           return false;
       }
    }

    var IsClassOrDefOrControlBlockType = function(blockCodeLineType) {
        if ( blockCodeLineType == BLOCK_CODELINE_TYPE.CLASS
             || blockCodeLineType == BLOCK_CODELINE_TYPE.DEF

             || blockCodeLineType == BLOCK_CODELINE_TYPE.IF 
             || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR
             || blockCodeLineType == BLOCK_CODELINE_TYPE.TRY
             || blockCodeLineType == BLOCK_CODELINE_TYPE.LAMBDA
             || blockCodeLineType == BLOCK_CODELINE_TYPE.WHILE ) {
            return true;
        } else {
            return false;
        }
    }

    var IsCodeBlockType = function(blockCodeLineType) {
        if ( blockCodeLineType == BLOCK_CODELINE_TYPE.CODE
            || blockCodeLineType == BLOCK_CODELINE_TYPE.PASS
            || blockCodeLineType == BLOCK_CODELINE_TYPE.CONTINUE 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.BREAK
            || blockCodeLineType == BLOCK_CODELINE_TYPE.PROPERTY
            
            || blockCodeLineType == BLOCK_CODELINE_TYPE.BLANK
            || blockCodeLineType == BLOCK_CODELINE_TYPE.COMMENT  ) {
            return true;
        } else {
            return false;
        }
    }
       /**
     * types에 해당하는 데이터유형을 가진 변수 목록 조회
     * @param {*} types 조회할 변수들의 데이터유형 목록
     * @param {*} callback 조회 후 실행할 callback. parameter로 result를 받는다
     */

    var LoadVariableList = function(blockContainer) {
        var types = [
            // pandas 객체
            'DataFrame', 'Series', 'Index', 'Period', 'GroupBy', 'Timestamp'
            // Index 하위 유형
            , 'RangeIndex', 'CategoricalIndex', 'MultiIndex', 'IntervalIndex', 'DatetimeIndex', 'TimedeltaIndex', 'PeriodIndex', 'Int64Index', 'UInt64Index', 'Float64Index'
            // GroupBy 하위 유형
            , 'DataFrameGroupBy', 'SeriesGroupBy'
            // Plot 관련 유형
            , 'Figure', 'AxesSubplot'
            // Numpy
            , 'ndarray'
            // Python 변수
            , 'str', 'int', 'float', 'bool', 'dict', 'list', 'tuple'
        ];
        /**
         * 변수 조회 시 제외해야할 변수명
         */
        var _VP_NOT_USING_VAR = ['_html', '_nms', 'NamespaceMagics', '_Jupyter', 'In', 'Out', 'exit', 'quit', 'get_ipython'];
        /**
         * 변수 조회 시 제외해야할 변수 타입
         */
        var _VP_NOT_USING_TYPE = ['module', 'function', 'builtin_function_or_method', 'instance', '_Feature', 'type', 'ufunc'];

        // types에 맞는 변수목록 조회하는 명령문 구성
        var cmdSB = new sb.StringBuilder();
        cmdSB.append(`print([{'varName': v, 'varType': type(eval(v)).__name__}`);
        cmdSB.appendFormat(`for v in dir() if (v not in {0}) `, JSON.stringify(_VP_NOT_USING_VAR));
        cmdSB.appendFormat(`& (type(eval(v)).__name__ not in {0}) `, JSON.stringify(_VP_NOT_USING_TYPE));
        cmdSB.appendFormat(`& (type(eval(v)).__name__ in {0})])`, JSON.stringify(types));

        // FIXME: vpFuncJS에만 kernel 사용하는 메서드가 정의되어 있어서 임시로 사용
        vp_executePython(cmdSB.toString(), function(result) {
            // callback(result);
            blockContainer.setKernelLoadedVariableList(result);
        });
    }

    /**
     * FIXME: vpFuncJS에만 kernel 사용하는 메서드가 정의되어 있어서 임시로 사용
     * @param {*} command 
     * @param {*} callback 
     * @param {*} isSilent 
     */
    var vp_executePython = function (command, callback, isSilent = false) {
        Jupyter.notebook.kernel.execute(
            command,
            {
                iopub: {
                    output: function (msg) {
                        var result = String(msg.content["text"]);
                        /** parsing */
                        var jsonVars = result.replace(/'/gi, `"`);
                        var varList = JSON.parse(jsonVars);

                        /** '_' 가 들어간 변수목록 제거 */
                        var filteredVarlist = varList.filter(varData => {
                            if (varData.varName.indexOf('_') != -1) {
                                return false;
                            } else {
                                return true;
                            }
                        });
                        callback(filteredVarlist);
                    }
                }
            },
            { silent: isSilent }
        );
    };
    return {
        ChangeOldToNewState
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

        , PxStrToNum

        , GenerateAPIBlockCode

        , AssertError
        
        , MapNewLineStrToSpacebar
        
        , ControlToggleInput
        , SetTextareaLineNumber_apiBlock

        , IsCanHaveIndentBlock
        , IsClassOrDefOrControlBlockType
        , IsCodeBlockType

        , LoadVariableList
    }
});
