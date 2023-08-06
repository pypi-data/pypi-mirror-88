define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'

    , 'nbextensions/visualpython/src/common/vpFuncJS'
    , 'nbextensions/visualpython/src/pandas/common/commonPandas'
    , 'nbextensions/visualpython/src/common/vpMakeDom'

    , '../../api.js'    
    , '../../config.js'
    , '../../constData.js'
    , '../../blockRenderer.js'
    
], function ( $, vpCommon, vpConst, sb, 
              vpFuncJS, libPandas, vpMakeDom,
              api, config, constData, blockRenderer ) {
    // FIXME: cell metadata test / 전역으로 말고 불러오기/덮어쓰기로 수정
    var _VP_CODEMD = {};

    /**
     * 코드 실행 후 결과값 보여주기 여부
     */
    var _VP_SHOW_RESULT = true;
        // 조회가능한 변수 data type 정의 FIXME: 조회 필요한 변수 유형 추가


    /**
     * types에 해당하는 데이터유형을 가진 변수 목록 조회
     * @param {*} types 조회할 변수들의 데이터유형 목록
     * @param {*} callback 조회 후 실행할 callback. parameter로 result를 받는다
     */
    var vp_searchVarList = function(callback) {
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
            callback(result);
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
                        console.log(filteredVarlist);
                    }
                }
            },
            { silent: isSilent }
        );
    };

    // /**
    //  * 알맞은 type 목록을 select 태그로 반환
    //  * @param {object} tag 
    //  * @param {Array<string>} types 
    //  * @param {string} defaultValue 
    //  */
    // var vp_generateVarSelect = function(tag, types, defaultValue = '') {
    //     // Index 는 여러 유형의 Index 타입이 있어 하위 타입들도 포함 필요
    //     var INDEX_TYPES = ['RangeIndex', 'CategoricalIndex', 'MultiIndex', 'IntervalIndex', 'DatetimeIndex', 'TimedeltaIndex', 'PeriodIndex', 'Int64Index', 'UInt64Index', 'Float64Index'];
    //     // GroupBy 는 여러 유형의 GroupyBy 타입이 있어 하위 타입들도 포함시키기
    //     var GROUPBY_TYPES = ['DataFrameGroupBy', 'SeriesGroupBy']
    //     if (types.indexOf('Index') >= 0) {
    //         types = types.concat(INDEX_TYPES);
    //     }
    //     if (types.indexOf('GroupBy') >= 0) {
    //         types = types.concat(GROUPBY_TYPES);
    //     }

    //     vp_searchVarList(types, function (result) {
    //         var jsonVars = result.replace(/'/gi, `"`);
    //         var varList = JSON.parse(jsonVars);
            
    //         // option 태그 구성
    //         varList.forEach(listVar => {
    //             if (types.includes(listVar.varType) && listVar.varName[0] !== '_') {
    //                 var option = document.createElement('option');
    //                 $(option).attr({
    //                     'value':listVar.varName,
    //                     'text':listVar.varName
    //                 });
    //                 // cell metadata test : defaultValue에 따라서 selected 적용
    //                 if (listVar.varName == defaultValue) {
    //                     $(option).prop('selected', true);
    //                 }
    //                 option.append(document.createTextNode(listVar.varName));
    //                 $(tag).append(option);
    //             }
    //         });

    //         // val-multi 일 경우(select multiple) value list 등록
    //         var classname = $(tag).attr('class');
    //         if (classname == 'var-multi') {
    //             $(tag).val(defaultValue);
    //         }
    //     });
    // }
    
    return vp_searchVarList;
});


