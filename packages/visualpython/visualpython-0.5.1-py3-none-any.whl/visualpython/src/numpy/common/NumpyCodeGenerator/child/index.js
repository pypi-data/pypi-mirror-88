define ([
    'require'
    , './numpyImportCodegenerator'

    , './functionList/NpArrayCodeGenerator'
    , './functionList/NpArangeCodeGenerator'
    , './functionList/NpReshapeCodeGenerator'
    , './functionList/NpZerosCodeGenerator'
    , './functionList/NpOnesCodeGenerator'
    , './functionList/NpEmptyCodeGenerator'
    , './functionList/NpEyeCodeGenerator'
    , './functionList/NpIdentityCodeGenerator'
    , './functionList/NpLinalgInvCodeGenerator'
    , './functionList/NpDiagCodeGenerator'
    , './functionList/NpFlattenCodeGenerator'
    , './functionList/NpFullCodeGenerator'
    , './functionList/NpFlipCodeGenerator'
    , './functionList/NpTCodeGenerator'
    , './functionList/NpTransposeCodeGenerator'
    , './functionList/NpSwapaxesCodeGenerator'
    , './functionList/NpConcatenateCodeGenerator'
    , './functionList/NpDotCodeGenerator'
    , './functionList/NpSumCodeGenerator'
    , './functionList/NpProdCodeGenerator'
    , './functionList/NpDiffCodeGenerator'
    , './functionList/NpCopyCodeGenerator'
    , './functionList/NpLinspaceCodeGenerator'
    , './functionList/NpRavelCodeGenerator'
    , './functionList/NpSplitCodeGenerator'
    , './functionList/NpDsplitHsplitVsplitCodeGenerator'
    , './functionList/NpStackCodeGenerator'
    , './functionList/NpDstackHstackVstackCodeGenerator'

    , './operationList/NumpyIndexingCodeGenerator'
    , './operationList/MakeArrayCodeGenerator'

    , './universalFunctionList/UnaryArimethicCodeGenerator'
    , './universalFunctionList/BinaryArimethicCodeGenerator'
    , './universalFunctionList/BinaryComparatorCodeGenerator'
    , './universalFunctionList/UnaryLogicalCodeGenerator'

    , './universalFunctionList/LinearAlgebraCodeGenerator'
    , './universalFunctionList/NpLinalgSolveGenerator'

    , './universalFunctionList/TrigonometricCodeGenerator'

    , './universalFunctionList/NpRandomRandintCodeGenerator'
    , './universalFunctionList/NpRandomRandCodeGenerator'

    , './statisticsList/NpMeanVarStdMaxMinMedianPercentileCodeGenerator'
    , './statisticsList/NumpyModeCodeGenerator'

], function( requirejs, 
             NumpyImportCodegenerator,

             NpArrayCodeGenerator, NpArangeCodeGenerator, NpReshapeCodeGenerator, NpZerosCodeGenerator, NpOnesCodeGenerator,
             NpEmptyCodeGenerator, NpEyeCodeGenerator, NpIdentityCodeGenerator, NpLinalgInvCodeGenerator, NpDiagCodeGenerator,
             NpFlattenCodeGenerator, NpFullCodeGenerator, NpFlipCodeGenerator, NpTCodeGenerator, NpTransposeCodeGenerator,
             NpSwapaxesCodeGenerator, NpConcatenateCodeGenerator, NpDotCodeGenerator, NpSumCodeGenerator, NpProdCodeGenerator, 
             NpDiffCodeGenerator, NpCopyCodeGenerator, NpLinspaceCodeGenerator, NpRavelCodeGenerator, NpSplitCodeGenerator, NpDsplitHsplitVsplitCodeGenerator,
             NpStackCodeGenerator, NpDstackHstackVstackCodeGenerator, 
             
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
             NumpyModeCodeGenerator,

            ) {

    return {
        NumpyImportCodegenerator,

        NpArrayCodeGenerator, NpArangeCodeGenerator, NpReshapeCodeGenerator, NpZerosCodeGenerator, NpOnesCodeGenerator,
        NpEmptyCodeGenerator, NpEyeCodeGenerator, NpIdentityCodeGenerator, NpLinalgInvCodeGenerator, NpDiagCodeGenerator,
        NpFlattenCodeGenerator, NpFullCodeGenerator, NpFlipCodeGenerator, NpTCodeGenerator, NpTransposeCodeGenerator,
        NpSwapaxesCodeGenerator, NpConcatenateCodeGenerator, NpDotCodeGenerator, NpSumCodeGenerator, NpProdCodeGenerator, 
        NpDiffCodeGenerator, NpCopyCodeGenerator, NpLinspaceCodeGenerator, NpRavelCodeGenerator, NpSplitCodeGenerator, NpDsplitHsplitVsplitCodeGenerator,
        NpStackCodeGenerator, NpDstackHstackVstackCodeGenerator,

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
        NumpyModeCodeGenerator,
    }
});
