define ([
    'require'
    , './functionList/NpArrayCodeValidator'
    , './functionList/NpArangeCodeValidator'
    , './functionList/NpReshapeCodeValidator'
    , './functionList/NpZerosCodeValidator'
    , './functionList/NpOnesCodeValidator'
    , './functionList/NpEmptyCodeValidator'
    , './functionList/NpEyeCodeValidator'
    , './functionList/NpIdentityCodeValidator'
    , './functionList/NpLinalgInvCodeValidator'
    , './functionList/NpDiagCodeValidator'
    , './functionList/NpFlattenCodeValidator'
    , './functionList/NpFullCodeValidator'
    , './functionList/NpFlipCodeValidator'
    , './functionList/NpTCodeValidator'
    , './functionList/NpTransposeCodeValidator'
    , './functionList/NpSwapaxesCodeValidator'
    , './functionList/NpConcatenateCodeValidator'
    , './functionList/NpDotCodeValidator'
    , './functionList/NpSumCodeValidator'
    , './functionList/NpDiffCodeValidator'
    , './functionList/NpCopyCodeValidator'
    , './functionList/NpLinspaceCodeValidator'
    , './functionList/NpRavelCodeValidator'
    , './functionList/NpSplitCodeValidator'
    , './functionList/NpDsplitHsplitVsplitCodeValidator'
    , './functionList/NpStackCodeValidator'
    , './functionList/NpDstackHstackVstackCodeValidator'

    , './NumpyIndexingCodeValidator'

    , './universalFunctionList/UnaryArimethicCodeValidator'
    , './universalFunctionList/BinaryArimethicCodeValidator'
    , './universalFunctionList/BinaryComparatorCodeValidator'
    , './universalFunctionList/UnaryLogicalCodeValidator'

    , './statisticsList/NpMeanVarStdMaxMinMedianCodeValidator'
    , './statisticsList/NumpyModeCodeValidator'
    , './statisticsList/NpPercentileCodeValidator'

], function( requirejs, 
             NpArrayCodeValidator, NpArangeCodeValidator, NpReshapeCodeValidator, NpZerosCodeValidator, NpOnesCodeValidator,
             NpEmptyCodeValidator, NpEyeCodeValidator, NpIdentityCodeValidator, NpLinalgInvCodeValidator, NpDiagCodeValidator,
             NpFlattenCodeValidator, NpFullCodeValidator, NpFlipCodeValidator, NpTCodeValidator, NpTransposeCodeValidator,
             NpSwapaxesCodeValidator, NpConcatenateCodeValidator, NpDotCodeValidator, NpSumCodeValidator, NpDiffCodeValidator,
             NpCopyCodeValidator, NpLinspaceCodeValidator, NpRavelCodeValidator, NpSplitCodeValidator, NpDsplitHsplitVsplitCodeValidator, NpStackCodeValidator,
             NpDstackHstackVstackCodeValidator,
             
             NumpyIndexingCodeValidator,
             
             UnaryArimethicCodeValidator, BinaryArimethicCodeValidator, BinaryComparatorCodeValidator, UnaryLogicalCodeValidator,

             NpMeanVarStdMaxMinMedianCodeValidator, NumpyModeCodeValidator, NpPercentileCodeValidator ) {
    return {
        NpArrayCodeValidator, NpArangeCodeValidator, NpReshapeCodeValidator, NpZerosCodeValidator, NpOnesCodeValidator,
        NpEmptyCodeValidator, NpEyeCodeValidator, NpIdentityCodeValidator, NpLinalgInvCodeValidator, NpDiagCodeValidator,
        NpFlattenCodeValidator, NpFullCodeValidator, NpFlipCodeValidator, NpTCodeValidator, NpTransposeCodeValidator,
        NpSwapaxesCodeValidator, NpConcatenateCodeValidator, NpDotCodeValidator, NpSumCodeValidator, NpDiffCodeValidator,
        NpCopyCodeValidator, NpLinspaceCodeValidator, NpRavelCodeValidator, NpSplitCodeValidator, NpDsplitHsplitVsplitCodeValidator, NpStackCodeValidator,
        NpDstackHstackVstackCodeValidator,

        NumpyIndexingCodeValidator,

        UnaryArimethicCodeValidator, BinaryArimethicCodeValidator, BinaryComparatorCodeValidator, UnaryLogicalCodeValidator,

        NpMeanVarStdMaxMinMedianCodeValidator, NumpyModeCodeValidator, NpPercentileCodeValidator,
    
    }
});
