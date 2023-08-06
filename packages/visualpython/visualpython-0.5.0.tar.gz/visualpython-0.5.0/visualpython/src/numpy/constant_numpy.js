define([
    'require'
    , 'nbextensions/visualpython/src/numpy/common/NumpyCodeGenerator/child/index'
    , 'nbextensions/visualpython/src/numpy/common/NumpyPageRender/child/index'
    , 'nbextensions/visualpython/src/numpy/common/numpyState'
], function( requirejs, 
             numpyCodeGeneratorList, numpyPageRenderList, NumpyStateGenerator ) {
    'use strict';

    const { NumpyImportCodegenerator,

            NpArrayCodeGenerator, NpArangeCodeGenerator, NpReshapeCodeGenerator, NpZerosCodeGenerator, NpOnesCodeGenerator,
            NpEmptyCodeGenerator, NpEyeCodeGenerator, NpIdentityCodeGenerator, NpDiagCodeGenerator, NpLinalgInvCodeGenerator,
            NpFlattenCodeGenerator, NpFullCodeGenerator, NpFlipCodeGenerator, NpTCodeGenerator, NpTransposeCodeGenerator,
            NpSwapaxesCodeGenerator, NpConcatenateCodeGenerator, NpDotCodeGenerator, NpSumCodeGenerator, NpProdCodeGenerator, NpDiffCodeGenerator,
            NpCopyCodeGenerator, NpLinspaceCodeGenerator, NpRavelCodeGenerator, NpSplitCodeGenerator, NpDsplitHsplitVsplitCodeGenerator, NpStackCodeGenerator,
            NpDstackHstackVstackCodeGenerator,
            
            NumpyIndexingCodeGenerator, 
            MakeArrayCodeGenerator,

            UnaryArimethicCodeGenerator,
            BinaryArimethicCodeGenerator,
            BinaryComparatorCodeGenerator,
            UnaryLogicalCodeGenerator,
            LinearAlgebraCodeGenerator,
            NpLinalgSolveGenerator,
            TrigonometricCodeGenerator,

            NpRandomRandintCodeGenerator,
            NpRandomRandCodeGenerator,

            NpMeanVarStdMaxMinMedianPercentileCodeGenerator,
        } = numpyCodeGeneratorList;

    const { NpImportRender,
            NpArangePageRender, NpArrayPageRender, NpReshapePageRender, NpZerosOnesEmptyPageRender, NpEyePageRender,
            NpIdentityPageRender, NpDiagPageRender, NpLinalgInvPageRender, NpFullPageRender, NpFlattenPageRender, NpFlipPageRender, NpTPageRender,
            NpTransposePageRender, NpSwapaxesCodeRender, NpDotPageRender, NpSumPageRender, NpConcatenatePageRender, NpDiffPageRender,
            NpCopyPageRender, NpLinspacePageRender, NpRavelPageRender, NpSplitPageRender, NpDsplitHsplitVsplitPageRender, NpStackPageRender, NpDstackHstackVstackPageRender,
            NumpyIndexingPageRender, 
            NpMeanVarStdMaxMinMedianPercentilePageRender,

            UnaryArimethicPageRender,
            BinaryArimethicPageRender,
            BinaryComparatorPageRender,
            UnaryLogicalPageRender,
            LinearAlgebraRender,
            NpLinalgSolveRender,
            TrigonometricPageRender,
            
            NpRandomRandintRender,
            NpRandomRandRender
            } = numpyPageRenderList;

    /** 
     * Numpy 패키지 데이터 타입
     */
    const numpyDtypeArray = [
        {
            name: 'None',
            value: 'None'
        },
        {
            name: 'Int8',
            value: 'np.int8'
        },
        {
            name: 'Int16',
            value: 'np.int16'
        },
        {
            name: 'Int32',
            value: 'np.int32'
        },
        {
            name: 'Int64',
            value: 'np.int64'
        },
        {
            name: 'Intp',
            value: 'np.intp'
        },
        {
            name: 'uInt8',
            value: 'np.uint8'
        },
        {
            name: 'uInt16',
            value: 'np.uint16'
        },
        {
            name: 'uInt32',
            value: 'np.uint32'
        },
        {
            name: 'uInt64',
            value: 'np.uint64'
        },
        {
            name: 'Float16',
            value: 'np.float16'
        },
        {
            name: 'Float32',
            value: 'np.float32'
        },
        {
            name: 'Float64',
            value: 'np.float64'
        },
        {
            name: 'Bool',
            value: 'np.bool'
        },
        {
            name: 'String',
            value: 'np.string_'
        }
    ];
    /**
     * Numpy 패키지 데이터 타입
     * value 앞에 np가 빠진 버전
     */
    const numpyBriefDtype = [
        {
            name: 'None',
            value: 'None'
        },
        {
            name: 'Int8',
            value: 'int8'
        },
        {
            name: 'Int16',
            value: 'int16'
        },
        {
            name: 'Int32',
            value: 'int32'
        },
        {
            name: 'Int64',
            value: 'int64'
        },
        {
            name: 'uInt8',
            value: 'uint8'
        },
        {
            name: 'uInt16',
            value: 'uint16'
        },
        {
            name: 'uInt32',
            value: 'uint32'
        },
        {
            name: 'uInt64',
            value: 'uint64'
        },
        {
            name: 'Float16',
            value: 'float16'
        },
        {
            name: 'Float32',
            value: 'float32'
        },
        {
            name: 'Float64',
            value: 'float64'
        },
        {
            name: 'Complex64',
            value: 'complex64'
        },
        {
            name: 'Complex128',
            value: 'complex128'
        },
        {
            name: 'Complex256',
            value: 'complex256'
        },
        {
            name: 'Bool',
            value: 'bool'
        },
        {
            name: 'String',
            value: 'string_'
        },
        {
            name: 'Object',
            value: 'object'
        }
    ];

    const numpyComparisonoperator = [
        {
            name: '<',
            value: '<'
        },
        {
            name: '<=',
            value: '<='
        },
        {
            name: '>',
            value: '>'
        },
        {
            name: '=>',
            value: '=>'
        },
        {
            name: '==',
            value: '=='
        },
        {
            name: '!=',
            value: '!='
        }
    ]

    const numpyUnaryoperator = [
        {
            name: '&',
            value: '&'
        },
        {
            name: '~',
            value: '~'
        },
        {
            name: '@',
            value: '@'
        },
        {
            name: '|',
            value: '|'
        },
        {
            name: '||',
            value: '||'
        }
    ]

    const numpyAxisArray = [
        '0','1','2','3','4','5','6','7','8','9','10','-1','-2','-3','-4','-5','-6','-7','-8','-9'
    ];

    const numpyIndexN = [
        '0','1','2','3','4','5','6','7','8','9','10'
    ];

    const numpyTrueFalseArray = [ 
        'True'
        , 'False'
    ]

    const numpyRavelOrderArray = [ 
        'C'
        , 'F'
        , 'K'
    ]

    const numpyEnumRenderEditorFuncType = {
        PARAM_ONE_ARRAY_EDITOR_TYPE: 0,
        PARAM_TWO_ARRAY_EDITOR_TYPE: 1,
        PARAM_THREE_ARRAY_EDITOR_TYPE: 2,
        PARAM_INPUT_EDITOR_TYPE: 3,
        PARAM_ONE_ARRAY_INDEX_N_EDITOR_TYPE: 4,
        PARAM_INDEXING_EDITOR_TYPE: 5
    }
    
    const numpyOptionObj = {
        numpyDtypeArray
        , numpyAxisArray
        , numpyIndexN
        , numpyIndexValueArray: numpyIndexN
        , numpyComparisonoperator
        , numpyUnaryoperator
        , numpyEnumRenderEditorFuncType
        , numpyTrueFalseArray
        , numpyRavelOrderArray
    }

    // numpy패키지 path string
    const numpyBaseCssPath = 'numpy/index.css';

    // numpy패키지 const 상수 string
    const STR_NULL = '';
    const STR_NUMPY_HTML_URL_PATH = 'numpy/pageList/index.html';

    const NP_STR_NULL = '';
    const NP_STR_EVENTTYPE_CHANGE_KEYUP_PASTE = 'change keyup paste';

    const NP_STR_ARRAY_ENG = 'array';
    const NP_STR_ARANGE_ENG = 'arange';
    const NP_STR_CONCATENATE_ENG = 'concatenate';
    const NP_STR_COPY_ENG = 'copy';
    
    const NP_STR_NP_ARRAY_ENG = 'np.array';
    const NP_STR_NP_ARANGE_ENG = 'np.arange';
    const NP_STR_NP_CONCATENATE_ENG = 'np.concatenate';
    const NP_STR_NP_COPY_ENG = 'np.copy';
    
    const NP_STR_INPUTED_KOR = '입력된';
    const NP_STR_CODE_KOR = '코드';
    const NP_STR_INFORMATION_KOR = '정보';

    const STR_CHANGE_KEYUP_PASTE = 'change keyup paste';
    /**
     * Numpy 함수 코드를 만드는 설계도
     */

    const numpyFunctionBluePrintList = [
        {
            funcName: 'import'
            , funcId: 'JY0'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NumpyImportCodegenerator
            // , numpyCodeValidator: NumpyCodeValidator
            , numpyPageRender: NpImportRender
            , numpyStateGenerator:  NumpyStateGenerator
            , state: {
                acronyms: 'np'
            }
        },
        {
            funcName: 'np_array'
            , funcId: 'np_array'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpArrayCodeGenerator
            // , numpyCodeValidator: NpArrayCodeValidator
            , numpyPageRender: NpArrayPageRender
            , numpyStateGenerator:  NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_arange'
            , funcId: 'np_arange'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpArangeCodeGenerator
            // , numpyCodeValidator: NpArangeCodeValidator
            , numpyPageRender: NpArangePageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None',
                paramOption: '1',
                paramData:{
                    paramOption1DataStart: '',
    
                    paramOption2DataStart: '',
                    paramOption2DataStop: '',
    
                    paramOption3DataStart: '',
                    paramOption3DataStop: '',
                    paramOption3DataStep: '',
                },
    
                returnVariable:'',
                isReturnVariable: false,
    
                makedCodeStr:'',
            }
        },
        {
            funcName: 'np_reshape'
            , funcId: 'np_reshape'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpReshapeCodeGenerator
            // , numpyCodeValidator: NpReshapeCodeValidator
            , numpyPageRender: NpReshapePageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None',
                paramOption: '1',
                paramData:{
                    paramOption1DataLength: '',
    
                    paramOption2DataRow: '',
                    paramOption2DataCol: '',
    
                    paramOption3DataRow: '',
                    paramOption3DataCol: '',
                    paramOption3DataDepth: '',
                },
                callVariable: '',
                returnVariable: '',
                isReturnVariable: false,
    
                makedCodeStr:'',
            }
        },
        {
            funcName: 'np_zeros'
            , funcId: 'np_zeros'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpZerosCodeGenerator
            // , numpyCodeValidator: NpZerosCodeValidator
            , numpyPageRender: NpZerosOnesEmptyPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOption1DataLength: '',
    
                    paramOption2DataRow: '',
                    paramOption2DataCol: '',
    
                    paramOption3DataArray: ['0'],
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_ones'
            , funcId: 'np_ones'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpOnesCodeGenerator
            // , numpyCodeValidator: NpOnesCodeValidator
            , numpyPageRender: NpZerosOnesEmptyPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOption1DataLength: '',
    
                    paramOption2DataRow: '',
                    paramOption2DataCol: '',
    
                    paramOption3DataArray: ['0'],
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_empty'
            , funcId: 'np_empty'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpEmptyCodeGenerator
            // , numpyCodeValidator: NpEmptyCodeValidator
            , numpyPageRender: NpZerosOnesEmptyPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOption1DataLength: '',
    
                    paramOption2DataRow: '',
                    paramOption2DataCol: '',
    
                    paramOption3DataArray: ['0'],
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_eye'
            , funcId: 'np_eye'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpEyeCodeGenerator
            // , numpyCodeValidator: NpEyeCodeValidator
            , numpyPageRender: NpEyePageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'

                , paramData:{
                    paramRowCol: '',
                    paramKIndex: '0',
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_identity'
            , funcId: 'np_identity'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpIdentityCodeGenerator
            // , numpyCodeValidator: NpIdentityCodeValidator
            , numpyPageRender: NpIdentityPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'

                , paramData:{
                    paramRowCol: '',
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_diag'
            , funcId: 'np_diag'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpDiagCodeGenerator
            // , numpyCodeValidator: NpDiagCodeValidator
            , numpyPageRender: NpDiagPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramVariable: ''
                }
                , indexK: '0'
                , returnVariable: ''
                , isReturnVariable: false
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_linalg_inv'
            , funcId: 'np_linalg_inv'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpLinalgInvCodeGenerator
            // , numpyCodeValidator: NpLinalgInvCodeValidator
            , numpyPageRender:  NpLinalgInvPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramVariable: '',
                    paramTwoArray: [['0']],
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_full'
            , funcId: 'np_full'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpFullCodeGenerator
            // , numpyCodeValidator: NpFullCodeValidator
            , numpyPageRender: NpFullPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOption1DataLength: '',
    
                    paramOption2DataRow: '',
                    paramOption2DataCol: '',
    
                    paramOption3DataArray: ['0'],
                }
                , indexValue: ''
                , returnVariable: ''
                , isReturnVariable: false
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_flip'
            , funcId: 'np_flip'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpFlipCodeGenerator
            // , numpyCodeValidator: NpFlipCodeValidator
            , numpyPageRender: NpFlipPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                axis:'0',
                paramData:{
                    paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_flatten'
            , funcId: 'np_flatten'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpFlattenCodeGenerator
            // , numpyCodeValidator: NpFlattenCodeValidator
            , numpyPageRender: NpFlattenPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'

                , paramData:{
                
                }
                , returnVariable: ''
                , isReturnVariable: false
                , callVariable: ''
                , makedCodeStr: ''
            }
        },
        {
            funcName: 'np_T'
            , funcId: 'np_T'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpTCodeGenerator
            // , numpyCodeValidator: NpTCodeValidator
            , numpyPageRender: NpTPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramData:{
               
                }
                , callVariable: ''
                , returnVariable: ''
                , isReturnVariable: false
                , makedCodeStr:''
            }
        },
        {
            funcName: 'np_transpose'
            , funcId: 'np_transpose'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpTransposeCodeGenerator
            // , numpyCodeValidator: NpTransposeCodeValidator
            , numpyPageRender: NpTransposePageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
    
                    paramOption1Axis1: '',
                    paramOption1Axis2: '',
    
                    paramOption2Axis1: '',
                    paramOption2Axis2: '',
                    paramOption2Axis3: '',
    
                    paramOption3AxisArray: ['0'],

                    paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , makedCodeStr:''
            }
        },
        {
            funcName: 'np_swapaxes'
            , funcId: 'np_swapaxes'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpSwapaxesCodeGenerator
            // , numpyCodeValidator: NpSwapaxesCodeValidator
            , numpyPageRender: NpSwapaxesCodeRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramData:{
                    paramAxis1: '',
                    paramAxis2: '',

                    paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , makedCodeStr:''
            }
        },
        {
            funcName: 'np_dot'
            , funcId: 'np_dot'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 2
            , numpyCodeGenerator: NpDotCodeGenerator
            // , numpyCodeValidator: NpDotCodeValidator
            , numpyPageRender: NpDotPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption1: '1'
                , paramOption2: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
    
                    , param2OneArray: ['0']
                    , param2TwoArray: [['0']]
                    , param2ThreeArray: [[['0']]]
                    , param2Scalar: ''
                    , param2Variable: '' 
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_concatenate'
            , funcId: 'np_concatenate'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpConcatenateCodeGenerator
            // , numpyCodeValidator: NpConcatenateCodeValidator
            , numpyPageRender: NpConcatenatePageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                axis: '0'
                , paramOption: '1'
                , paramData:{
                    paramOption1ParamVariable1: ''
                    , paramOption1ParamVariable2: ''
    
                    , paramOption2ParamVariable1: ''
                    , paramOption2ParamVariable2: ''
                    , paramOption2ParamVariable3: ''
    
                    , paramOption3ParamVariableArray: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_sum'
            , funcId: 'np_sum'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpSumCodeGenerator
            // , numpyCodeValidator: NpSumCodeValidator
            , numpyPageRender: NpSumPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                axis: '0'
                , paramData:{
                    paramVariable: '',
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , makedCodeStr:''
            }
        },
        {
            funcName: 'np_prod'
            , funcId: 'np_prod'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpProdCodeGenerator
            // , numpyCodeValidator: NpSumCodeValidator
            , numpyPageRender: NpSumPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                axis: '0'
                , paramData:{
                    paramVariable: '',
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , makedCodeStr:''
            }
        },
        {
            funcName: 'np_diff'
            , funcId: 'np_diff'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpDiffCodeGenerator
            // , numpyCodeValidator: NpDiffCodeValidator
            , numpyPageRender: NpDiffPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                indexN: '0'
                , paramData:{
                    paramVariable: '',
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , makedCodeStr:''
            }
        },
        {
            funcName: 'np_linspace'
            , funcId: 'np_linspace'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpLinspaceCodeGenerator
            // , numpyCodeValidator: NpLinspaceCodeValidator
            , numpyPageRender: NpLinspacePageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramData:{
                    paramStart: ''
                    , paramStop: ''
                    , paramNum: ''
                    , paramEndpoint: 'True'
                    , paramRetstep: 'True'
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , makedCodeStr:''
            }
        },
        {
            funcName: 'np_copy'
            , funcId: 'np_copy'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpCopyCodeGenerator
            // , numpyCodeValidator: NpCopyCodeValidator
            , numpyPageRender: NpCopyPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramData:{
                    paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , makedCodeStr: ''
            }
        },
        {
            funcName: 'np_ravel'
            , funcId: 'np_ravel'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpRavelCodeGenerator
            // , numpyCodeValidator: NpRavelCodeValidator
            , numpyPageRender: NpRavelPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                order: 'C'
                , paramData:{
                    paramVariable: '',
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , makedCodeStr:''
            }
        },
        {
            funcName: 'np_split'
            , funcId: 'np_split'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpSplitCodeGenerator
            // , numpyCodeValidator: NpSplitCodeValidator
            , numpyPageRender: NpSplitPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                axis: '0',
                paramOption: '1',
                paramData:{
                    paramOption1DataLength: '', 
                    paramOption2DataRow: '', paramOption2DataCol: '',
                    paramOption3DataRow: '', paramOption3DataCol: '', paramOption3DataDepth: '',
                    paramOption4DataArray: ['','','','',],

                    paramVariable: '',
                },
    
                returnVariable: '',
                isReturnVariable: false,
    
                makedCodeStr:'',
            }
        }, 
        {
            funcName: 'np_dsplit'
            , funcId: 'np_dsplit'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpDsplitHsplitVsplitCodeGenerator
            // , numpyCodeValidator: NpDsplitHsplitVsplitCodeValidator
            , numpyPageRender: NpDsplitHsplitVsplitPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1',
                paramData:{
                    paramOption1DataLength: '', 
                    paramOption2DataRow: '', paramOption2DataCol: '',
                    paramOption3DataRow: '', paramOption3DataCol: '', paramOption3DataDepth: '',
                    paramOption4DataArray: ['','','','',],
                    paramVariable: ''
                },
                returnVariable: '',
                isReturnVariable: false,
                funcId: 'JY26',
                
                makedCodeStr:'',
            }
        },
        {
            funcName: 'np_hsplit'
            , funcId: 'np_hsplit'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpDsplitHsplitVsplitCodeGenerator
            // , numpyCodeValidator: NpDsplitHsplitVsplitCodeValidator
            , numpyPageRender: NpDsplitHsplitVsplitPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1',
                paramData:{
                    paramOption1DataLength: '', 
                    paramOption2DataRow: '', paramOption2DataCol: '',
                    paramOption3DataRow: '', paramOption3DataCol: '', paramOption3DataDepth: '',
                    paramOption4DataArray: ['','','','',],
                    paramVariable: ''
                },
                returnVariable: '',
                isReturnVariable: false,
                funcId: 'JY27',
                
                makedCodeStr:'',
            }
        },
        {
            funcName: 'np_vsplit'
            , funcId: 'np_vsplit'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpDsplitHsplitVsplitCodeGenerator
            // , numpyCodeValidator: NpDsplitHsplitVsplitCodeValidator
            , numpyPageRender: NpDsplitHsplitVsplitPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1',
                paramData:{
                    paramOption1DataLength: '', 
                    paramOption2DataRow: '', paramOption2DataCol: '',
                    paramOption3DataRow: '', paramOption3DataCol: '', paramOption3DataDepth: '',
                    paramOption4DataArray: ['','','','',],
                    paramVariable: ''
                },
                returnVariable: '',
                isReturnVariable: false,
                funcId: 'JY28',
                
                makedCodeStr:'',
            }
        },
        {
            funcName: 'np_stack'
            , funcId: 'np_stack'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpStackCodeGenerator
            // , numpyCodeValidator: NpStackCodeValidator
            , numpyPageRender: NpStackPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                axis: '0',
                paramOption: '1',
                paramData:{
                    paramOption1DataLength: '', 
                    paramOption2DataRow: '', paramOption2DataCol: '',
                    paramOption3DataRow: '', paramOption3DataCol: '', paramOption3DataDepth: '',
                    paramOption4DataArray: ['','','','',]
                },
                returnVariable: '',
                isReturnVariable: false,
    
                makedCodeStr:'',
            }
        },

        {
            funcName: 'np_dstack'
            , funcId: 'np_dstack'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpDstackHstackVstackCodeGenerator
            // , numpyCodeValidator: NpDstackHstackVstackCodeValidator
            , numpyPageRender: NpDstackHstackVstackPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1',
                paramData:{
                    paramOption1DataLength: '', 
                    paramOption2DataRow: '', paramOption2DataCol: '',
                    paramOption3DataRow: '', paramOption3DataCol: '', paramOption3DataDepth: '',
                    paramOption4DataArray: ['','','','',]
                },
                returnVariable: '',
                isReturnVariable: false,
                funcId: 'JY30',
                
                makedCodeStr:'',
            }
        },
        {
            funcName: 'np_hstack'
            , funcId: 'np_hstack'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpDstackHstackVstackCodeGenerator
            // , numpyCodeValidator: NpDstackHstackVstackCodeValidator
            , numpyPageRender: NpDstackHstackVstackPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1',
                paramData:{
                    paramOption1DataLength: '', 
                    paramOption2DataRow: '', paramOption2DataCol: '',
                    paramOption3DataRow: '', paramOption3DataCol: '', paramOption3DataDepth: '',
                    paramOption4DataArray: ['','','','',]
                },
                returnVariable: '',
                isReturnVariable: false,
                funcId: 'JY31',
                
                makedCodeStr:'',
            }
        },
        {
            funcName: 'np_vstack'
            , funcId: 'np_vstack'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpDstackHstackVstackCodeGenerator
            // , numpyCodeValidator: NpDstackHstackVstackCodeValidator
            , numpyPageRender: NpDstackHstackVstackPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1',
                paramData:{
                    paramOption1DataLength: '', 
                    paramOption2DataRow: '', paramOption2DataCol: '',
                    paramOption3DataRow: '', paramOption3DataCol: '', paramOption3DataDepth: '',
                    paramOption4DataArray: ['','','','',]
                },
                returnVariable: '',
                isReturnVariable: false,
                funcId: 'JY32',
                
                makedCodeStr:'',
            }
        },

        {
            funcName: 'numpy Indexing'
            , funcId: 'JY100'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NumpyIndexingCodeGenerator
            // , numpyCodeValidator: NumpyIndexingCodeValidator
            , numpyPageRender: NumpyIndexingPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1'
                , paramData:{
                    paramOption1Start: '',
                    paramOption1End: '',

                    paramOption2RowStart: '',
                    paramOption2RowEnd: '',
                    paramOption2ColStart: '',
                    paramOption2ColEnd: '',

                    paramOption3Array: []
                }
                , callVariable: ''
                , returnVariable: ''
                , isReturnVariable: false

                , makedCodeStr: '',
            }
        },

        // numpy 통계 statisticsList
        {
            funcName: 'np_mean'
            , funcId: 'np_mean'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpMeanVarStdMaxMinMedianPercentileCodeGenerator
            // , numpyCodeValidator: NpMeanVarStdMaxMinMedianCodeValidator
            , numpyPageRender: NpMeanVarStdMaxMinMedianPercentilePageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY200'
                
                , makedCodeStr: '',
            }
        },


        {
            funcName: 'np.var'
            , funcId: 'JY201'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpMeanVarStdMaxMinMedianPercentileCodeGenerator
            // , numpyCodeValidator: NpMeanVarStdMaxMinMedianCodeValidator
            , numpyPageRender: NpMeanVarStdMaxMinMedianPercentilePageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY201'
                
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np.std'
            , funcId: 'JY202'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpMeanVarStdMaxMinMedianPercentileCodeGenerator
            // , numpyCodeValidator: NpMeanVarStdMaxMinMedianCodeValidator
            , numpyPageRender: NpMeanVarStdMaxMinMedianPercentilePageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY202'
                
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_max'
            , funcId: 'np_max'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpMeanVarStdMaxMinMedianPercentileCodeGenerator
            // , numpyCodeValidator: NpMeanVarStdMaxMinMedianCodeValidator
            , numpyPageRender: NpMeanVarStdMaxMinMedianPercentilePageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY203'
                
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_min'
            , funcId: 'JY204'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpMeanVarStdMaxMinMedianPercentileCodeGenerator
            // , numpyCodeValidator: NpMeanVarStdMaxMinMedianCodeValidator
            , numpyPageRender: NpMeanVarStdMaxMinMedianPercentilePageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY204'
                
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_median'
            , funcId: 'JY205'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpMeanVarStdMaxMinMedianPercentileCodeGenerator
            // , numpyCodeValidator: NpMeanVarStdMaxMinMedianCodeValidator
            , numpyPageRender: NpMeanVarStdMaxMinMedianPercentilePageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY205'
                
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np.percentile'
            , funcId: 'JY206'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpMeanVarStdMaxMinMedianPercentileCodeGenerator
            // , numpyCodeValidator: NpPercentileCodeValidator
            , numpyPageRender: NpMeanVarStdMaxMinMedianPercentilePageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , axis: '0'
                , indexQ: ''
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY206'
                
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'numpyMode'
            , funcId: 'JY207'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpMeanVarStdMaxMinMedianPercentileCodeGenerator
            // , numpyCodeValidator: NpMeanVarStdMaxMinMedianCodeValidator
            , numpyPageRender: NpMeanVarStdMaxMinMedianPercentilePageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {

            }
        },
        {
            funcName: 'np.cov'
            , funcId: 'JY208'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpMeanVarStdMaxMinMedianPercentileCodeGenerator
            // , numpyCodeValidator: NpMeanVarStdMaxMinMedianCodeValidator
            , numpyPageRender: NpMeanVarStdMaxMinMedianPercentilePageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {

            }
        },
        {
            funcName: 'np.corrcoef'
            , funcId: 'JY209'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpMeanVarStdMaxMinMedianPercentileCodeGenerator
            // , numpyCodeValidator: NpMeanVarStdMaxMinMedianCodeValidator
            , numpyPageRender: NpMeanVarStdMaxMinMedianPercentilePageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {

            }
        },
        /**
         * 유니버설 함수
         */
        {
            funcName: 'np_abs'
            , funcId: 'np_abs'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: UnaryArimethicCodeGenerator
            // , numpyCodeValidator: UnaryArimethicCodeValidator
            , numpyPageRender: UnaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , funcId: 'JY300'
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_ceil'
            , funcId: 'np_ceil'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: UnaryArimethicCodeGenerator
            // , numpyCodeValidator: UnaryArimethicCodeValidator
            , numpyPageRender: UnaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , funcId: 'JY301'
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_exp'
            , funcId: 'np_exp'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: UnaryArimethicCodeGenerator
            // , numpyCodeValidator: UnaryArimethicCodeValidator
            , numpyPageRender: UnaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , funcId: 'JY302'
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_fabs'
            , funcId: 'np_fabs'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: UnaryArimethicCodeGenerator
            // , numpyCodeValidator: UnaryArimethicCodeValidator
            , numpyPageRender: UnaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , funcId: 'JY303'
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_floor'
            , funcId: 'np_floor'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: UnaryArimethicCodeGenerator
            // , numpyCodeValidator: UnaryArimethicCodeValidator
            , numpyPageRender: UnaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , funcId: 'JY304'
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_log'
            , funcId: 'np_log'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: UnaryArimethicCodeGenerator
            // , numpyCodeValidator: UnaryArimethicCodeValidator
            , numpyPageRender: UnaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , funcId: 'JY305'
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_log1p'
            , funcId: 'np_log1p'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: UnaryArimethicCodeGenerator
            // , numpyCodeValidator: UnaryArimethicCodeValidator
            , numpyPageRender: UnaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , funcId: 'JY306'
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_log2'
            , funcId: 'np_log2'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: UnaryArimethicCodeGenerator
            // , numpyCodeValidator: UnaryArimethicCodeValidator
            , numpyPageRender:  UnaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , funcId: 'JY307'
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_log10'
            , funcId: 'np_log10'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator:  UnaryArimethicCodeGenerator
            // , numpyCodeValidator: UnaryArimethicCodeValidator
            , numpyPageRender:  UnaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , funcId: 'JY308'
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_modf'
            , funcId: 'np_modf'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: UnaryArimethicCodeGenerator
            // , numpyCodeValidator: UnaryArimethicCodeValidator
            , numpyPageRender: UnaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , funcId: 'JY309'
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_rint'
            , funcId: 'np_rint'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: UnaryArimethicCodeGenerator
            // , numpyCodeValidator: UnaryArimethicCodeValidator
            , numpyPageRender: UnaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , funcId: 'JY310'
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_sqrt'
            , funcId: 'np_sqrt'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: UnaryArimethicCodeGenerator
            // , numpyCodeValidator: UnaryArimethicCodeValidator
            , numpyPageRender: UnaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , funcId: 'JY311'
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_square'
            , funcId: 'np_square'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: UnaryArimethicCodeGenerator
            // , numpyCodeValidator: UnaryArimethicCodeValidator
            , numpyPageRender: UnaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
    
                , funcId: 'JY312'
                , makedCodeStr: '',
            }
        },
        {
            funcName: 'np_add'
            , funcId: 'np_add'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: BinaryArimethicCodeGenerator
            // , numpyCodeValidator: BinaryArimethicCodeValidator
            , numpyPageRender: BinaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption1: '1'
                , paramOption2: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
    
                    , param2OneArray: ['0']
                    , param2TwoArray: [['0']]
                    , param2ThreeArray: [[['0']]]
                    , param2Scalar: ''
                    , param2Variable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY313'
            }
        },
        {
            funcName: 'np_divide'
            , funcId: 'np_divide'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: BinaryArimethicCodeGenerator
            // , numpyCodeValidator: BinaryArimethicCodeValidator
            , numpyPageRender: BinaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption1: '1'
                , paramOption2: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
    
                    , param2OneArray: ['0']
                    , param2TwoArray: [['0']]
                    , param2ThreeArray: [[['0']]]
                    , param2Scalar: ''
                    , param2Variable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY314'
            }
        },
        {
            funcName: 'np_floor_divide'
            , funcId: 'np_floor_divide'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: BinaryArimethicCodeGenerator
            // , numpyCodeValidator: BinaryArimethicCodeValidator
            , numpyPageRender: BinaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption1: '1'
                , paramOption2: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
    
                    , param2OneArray: ['0']
                    , param2TwoArray: [['0']]
                    , param2ThreeArray: [[['0']]]
                    , param2Scalar: ''
                    , param2Variable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY315'
                
            }
        },
        {
            funcName: 'np_fmax'
            , funcId: 'np_fmax'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: BinaryArimethicCodeGenerator
            // , numpyCodeValidator: BinaryArimethicCodeValidator
            , numpyPageRender: BinaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption1: '1'
                , paramOption2: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
    
                    , param2OneArray: ['0']
                    , param2TwoArray: [['0']]
                    , param2ThreeArray: [[['0']]]
                    , param2Scalar: ''
                    , param2Variable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY316'
                
            }
        },
        {
            funcName: 'np_fmin'
            , funcId: 'np_fmin'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: BinaryArimethicCodeGenerator
            // , numpyCodeValidator: BinaryArimethicCodeValidator
            , numpyPageRender: BinaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption1: '1'
                , paramOption2: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
    
                    , param2OneArray: ['0']
                    , param2TwoArray: [['0']]
                    , param2ThreeArray: [[['0']]]
                    , param2Scalar: ''
                    , param2Variable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY317'
                
            }
        },
        {
            funcName: 'np_maximum'
            , funcId: 'np_maximum'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: BinaryArimethicCodeGenerator
            // , numpyCodeValidator: BinaryArimethicCodeValidator
            , numpyPageRender: BinaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption1: '1'
                , paramOption2: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
    
                    , param2OneArray: ['0']
                    , param2TwoArray: [['0']]
                    , param2ThreeArray: [[['0']]]
                    , param2Scalar: ''
                    , param2Variable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY318'
                
            }
        },
        {
            funcName: 'np_minimum'
            , funcId: 'np_minimum'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: BinaryArimethicCodeGenerator
            // , numpyCodeValidator: BinaryArimethicCodeValidator
            , numpyPageRender: BinaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption1: '1'
                , paramOption2: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
    
                    , param2OneArray: ['0']
                    , param2TwoArray: [['0']]
                    , param2ThreeArray: [[['0']]]
                    , param2Scalar: ''
                    , param2Variable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY319'
                
            }
        },
        {
            funcName: 'np_mod'
            , funcId: 'np_mod'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: BinaryArimethicCodeGenerator
            // , numpyCodeValidator: BinaryArimethicCodeValidator
            , numpyPageRender: BinaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption1: '1'
                , paramOption2: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
    
                    , param2OneArray: ['0']
                    , param2TwoArray: [['0']]
                    , param2ThreeArray: [[['0']]]
                    , param2Scalar: ''
                    , param2Variable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY320'
                
            }
        },
        {
            funcName: 'np_multiply'
            , funcId: 'np_multiply'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: BinaryArimethicCodeGenerator
            // , numpyCodeValidator: BinaryArimethicCodeValidator
            , numpyPageRender: BinaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption1: '1'
                , paramOption2: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
    
                    , param2OneArray: ['0']
                    , param2TwoArray: [['0']]
                    , param2ThreeArray: [[['0']]]
                    , param2Scalar: ''
                    , param2Variable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY321'
                
            }
        },
        {
            funcName: 'np_power'
            , funcId: 'np_power'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: BinaryArimethicCodeGenerator
            // , numpyCodeValidator: BinaryArimethicCodeValidator
            , numpyPageRender: BinaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption1: '1'
                , paramOption2: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
    
                    , param2OneArray: ['0']
                    , param2TwoArray: [['0']]
                    , param2ThreeArray: [[['0']]]
                    , param2Scalar: ''
                    , param2Variable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY322'
                
            }
        },
        {
            funcName: 'np_subtract'
            , funcId: 'np_subtract'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: BinaryArimethicCodeGenerator
            // , numpyCodeValidator: BinaryArimethicCodeValidator
            , numpyPageRender: BinaryArimethicPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                dtype: 'None'
                , paramOption1: '1'
                , paramOption2: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
    
                    , param2OneArray: ['0']
                    , param2TwoArray: [['0']]
                    , param2ThreeArray: [[['0']]]
                    , param2Scalar: ''
                    , param2Variable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY323'
                
            }
        },
        {
            funcName: 'np_equal'
            , funcId: 'np_equal'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: BinaryComparatorCodeGenerator
            // , numpyCodeValidator: BinaryComparatorCodeValidator
            , numpyPageRender: BinaryComparatorPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption1: '1'
                , paramOption2: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
    
                    , param2OneArray: ['0']
                    , param2TwoArray: [['0']]
                    , param2ThreeArray: [[['0']]]
                    , param2Scalar: ''
                    , param2Variable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY324'
                
            }
        },
        {
            funcName: 'np_greater'
            , funcId: 'np_greater'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: BinaryComparatorCodeGenerator
            // , numpyCodeValidator: BinaryComparatorCodeValidator
            , numpyPageRender: BinaryComparatorPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption1: '1'
                , paramOption2: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
    
                    , param2OneArray: ['0']
                    , param2TwoArray: [['0']]
                    , param2ThreeArray: [[['0']]]
                    , param2Scalar: ''
                    , param2Variable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY325'
                
            }
        },
        {
            funcName: 'np_greater_equal'
            , funcId: 'np_greater_equal'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: BinaryComparatorCodeGenerator
            // , numpyCodeValidator: BinaryComparatorCodeValidator
            , numpyPageRender: BinaryComparatorPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption1: '1'
                , paramOption2: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
    
                    , param2OneArray: ['0']
                    , param2TwoArray: [['0']]
                    , param2ThreeArray: [[['0']]]
                    , param2Scalar: ''
                    , param2Variable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY326'
                
            }
        },
        {
            funcName: 'np_less'
            , funcId: 'np_less'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: BinaryComparatorCodeGenerator
            // , numpyCodeValidator: BinaryComparatorCodeValidator
            , numpyPageRender: BinaryComparatorPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption1: '1'
                , paramOption2: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
    
                    , param2OneArray: ['0']
                    , param2TwoArray: [['0']]
                    , param2ThreeArray: [[['0']]]
                    , param2Scalar: ''
                    , param2Variable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY327'
                
            }
        },
        {
            funcName: 'np_less_equal'
            , funcId: 'np_less_equal'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: BinaryComparatorCodeGenerator
            // , numpyCodeValidator: BinaryComparatorCodeValidator
            , numpyPageRender: BinaryComparatorPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption1: '1'
                , paramOption2: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
    
                    , param2OneArray: ['0']
                    , param2TwoArray: [['0']]
                    , param2ThreeArray: [[['0']]]
                    , param2Scalar: ''
                    , param2Variable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY328'
                
            }
        },
        {
            funcName: 'np_not_equal'
            , funcId: 'np_not_equal'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: BinaryComparatorCodeGenerator
            // , numpyCodeValidator: BinaryComparatorCodeValidator
            , numpyPageRender: BinaryComparatorPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
    
                paramOption1: '1'
                , paramOption2: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
    
                    , param2OneArray: ['0']
                    , param2TwoArray: [['0']]
                    , param2ThreeArray: [[['0']]]
                    , param2Scalar: ''
                    , param2Variable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY329'
                
            }
        },
        {
            funcName: 'np_all'
            , funcId: 'np_all'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: UnaryLogicalCodeGenerator
            // , numpyCodeValidator: UnaryLogicalCodeValidator
            , numpyPageRender: UnaryLogicalPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY330'
            }
        },
        {
            funcName: 'np_any'
            , funcId: 'np_any'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: UnaryLogicalCodeGenerator
            // , numpyCodeValidator: UnaryLogicalCodeValidator
            , numpyPageRender: UnaryLogicalPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY331'
            }
        },
        {
            funcName: 'np_isanan'
            , funcId: 'np_isanan'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: UnaryLogicalCodeGenerator
            // , numpyCodeValidator: UnaryLogicalCodeValidator
            , numpyPageRender: UnaryLogicalPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY332'
            }
        },
        {
            funcName: 'np_isfinite'
            , funcId: 'np_isfinite'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: UnaryLogicalCodeGenerator
            // , numpyCodeValidator: UnaryLogicalCodeValidator
            , numpyPageRender: UnaryLogicalPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY333'
            }
        },
        {
            funcName: 'np_isnan'
            , funcId: 'np_isnan'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: UnaryLogicalCodeGenerator
            // , numpyCodeValidator: UnaryLogicalCodeValidator
            , numpyPageRender: UnaryLogicalPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY334'
            }
        },
        {
            funcName: 'np_isinf'
            , funcId: 'np_isinf'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: UnaryLogicalCodeGenerator
            // , numpyCodeValidator: UnaryLogicalCodeValidator
            , numpyPageRender: UnaryLogicalPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY335'
            }
        },
        {
            funcName: 'np_isneginf'
            , funcId: 'np_isneginf'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: UnaryLogicalCodeGenerator
            // , numpyCodeValidator: UnaryLogicalCodeValidator
            , numpyPageRender: UnaryLogicalPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY336'
            }
        },
        {
            funcName: 'np_isposinf'
            , funcId: 'np_isposinf'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: UnaryLogicalCodeGenerator
            // , numpyCodeValidator: UnaryLogicalCodeValidator
            , numpyPageRender: UnaryLogicalPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY337'
            }
        },
        {
            funcName: 'np.logical_not'
            , funcId: 'JY338'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: UnaryLogicalCodeGenerator
            // , numpyCodeValidator: UnaryLogicalCodeValidator
            , numpyPageRender: UnaryLogicalPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY338'
            }
        },
        {
            funcName: 'np_linalg_det'
            , funcId: 'np_linalg_det'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: LinearAlgebraCodeGenerator
            // , numpyCodeValidator: NpArrayCodeValidator
            , numpyPageRender: LinearAlgebraRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY339'
            }
        },
        {
            funcName: 'np_linalg_eig'
            , funcId: 'np_linalg_eig'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: LinearAlgebraCodeGenerator
            // , numpyCodeValidator: NpArrayCodeValidator
            , numpyPageRender: LinearAlgebraRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY340'
            }
        },
        {
            funcName: 'np_linalg_svd'
            , funcId: 'JY341'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: LinearAlgebraCodeGenerator
            // , numpyCodeValidator: NpArrayCodeValidator
            , numpyPageRender: LinearAlgebraRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY341'
            }
        },
        {
            funcName: 'np.trace'
            , funcId: 'JY342'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: LinearAlgebraCodeGenerator
            // , numpyCodeValidator: NpArrayCodeValidator
            , numpyPageRender: LinearAlgebraRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY342'
            }
        },
        {
            funcName: 'np.linalg.solve'
            , funcId: 'JY343'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpLinalgSolveGenerator
            // , numpyCodeValidator: NpArrayCodeValidator
            , numpyPageRender: NpLinalgSolveRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption1: '1'
                , paramOption2: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
    
                    , param2OneArray: ['0']
                    , param2TwoArray: [['0']]
                    , param2ThreeArray: [[['0']]]
                    , param2Scalar: ''
                    , param2Variable: '' 
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY343'
            }
        },
        {
            funcName: 'np_sin'
            , funcId: 'np_sin'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: TrigonometricCodeGenerator
            // , numpyCodeValidator: NpArrayCodeValidator
            , numpyPageRender: TrigonometricPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY344'
            }
        },
        {
            funcName: 'np_cos'
            , funcId: 'np_cos'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: TrigonometricCodeGenerator
            // , numpyCodeValidator: NpArrayCodeValidator
            , numpyPageRender: TrigonometricPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY345'
            }
        },
        {
            funcName: 'np_tan'
            , funcId: 'np_tan'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: TrigonometricCodeGenerator
            // , numpyCodeValidator: NpArrayCodeValidator
            , numpyPageRender: TrigonometricPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY346'
            }
        },
        {
            funcName: 'np_arcsin'
            , funcId: 'np_arcsin'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: TrigonometricCodeGenerator
            // , numpyCodeValidator: NpArrayCodeValidator
            , numpyPageRender: TrigonometricPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY347'
            }
        },
        {
            funcName: 'np_arccos'
            , funcId: 'np_arccos'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: TrigonometricCodeGenerator
            // , numpyCodeValidator: NpArrayCodeValidator
            , numpyPageRender: TrigonometricPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY348'
            }
        },
        {
            funcName: 'np_arctan'
            , funcId: 'np_arctan'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: TrigonometricCodeGenerator
            // , numpyCodeValidator: NpArrayCodeValidator
            , numpyPageRender: TrigonometricPageRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                paramOption: '1'
                , paramData:{
                    paramOneArray: ['0']
                    , paramTwoArray: [['0']]
                    , paramThreeArray: [[['0']]]
                    , paramScalar: ''
                    , paramVariable: ''
                }
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY349'
            }
        },
        {
            funcName: 'np_random_randint'
            , funcId: 'JY350'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpRandomRandintCodeGenerator
            // , numpyCodeValidator: NumpyCodeValidator
            , numpyPageRender: NpRandomRandintRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                indexValue: ''
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY350'
            }
        },
        {
            funcName: 'np_random_rand'
            , funcId: 'JY351'
            , htmlUrlPath: 'numpy/pageList/index.html'
            , stepCount: 1
            , numpyCodeGenerator: NpRandomRandCodeGenerator
            // , numpyCodeValidator: NumpyCodeValidator
            , numpyPageRender: NpRandomRandRender
            , numpyStateGenerator: NumpyStateGenerator
            , state: {
                indexValue1: ''
                , indexValue2: ''
                , returnVariable: ''
                , isReturnVariable: false
                , funcId: 'JY351'
            }
        }
        
    ];
    const numpyPropMap = new Map();
    numpyFunctionBluePrintList.forEach( function(element) {
        numpyPropMap.set(element.funcId, {
            numpyCodeGenerator: element.numpyCodeGenerator
            // , numpyCodeValidator: element.numpyCodeValidator
            , numpyPageRender: element.numpyPageRender
            , numpyStateGenerator: element.numpyStateGenerator
            , htmlUrlPath: element.htmlUrlPath
            , state: element.state
            , numpyOptionObj: numpyOptionObj
        });
    });

    return { 
        STR_NULL
        , STR_NUMPY_HTML_URL_PATH
        // numpy 패키지에 사용될 매직 데이터, 함수 객체 들
        , NUMPY_DTYPE: numpyDtypeArray
        , NUMPY_BRIEF_DTYPE: numpyBriefDtype
        , NUMPY_AXIS: numpyAxisArray
        , NUMPY_FUNCTION_BLUEPRINT_LIST: numpyFunctionBluePrintList
        , NUMPY_PROP_MAP: numpyPropMap
        , ENUM_NUMPY_RENDER_EDITOR_FUNC_TYPE: numpyEnumRenderEditorFuncType
        // numpy 패키지 파일 PATH
        , NUMPY_BASE_CSS_PATH : numpyBaseCssPath
        , NUMPY_OPTION_OBJ : numpyOptionObj
        // numpy 패키지에 사용될 매직 상수 들
        , NP_STR_NULL
        , NP_STR_EVENTTYPE_CHANGE_KEYUP_PASTE

        , NP_STR_ARRAY_ENG
        , NP_STR_ARANGE_ENG
        , NP_STR_CONCATENATE_ENG
        , NP_STR_COPY_ENG
        , NP_STR_NP_ARRAY_ENG
        , NP_STR_NP_ARANGE_ENG
        , NP_STR_NP_CONCATENATE_ENG
        , NP_STR_NP_COPY_ENG

        , NP_STR_INPUTED_KOR
        , NP_STR_CODE_KOR
        , NP_STR_INFORMATION_KOR

        , STR_CHANGE_KEYUP_PASTE
    };
});

