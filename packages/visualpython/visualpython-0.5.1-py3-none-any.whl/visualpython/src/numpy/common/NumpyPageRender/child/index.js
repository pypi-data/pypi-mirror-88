define ([
    'require'
    , './npImportRender'

    , './functionList/NpArangePageRender'
    , './functionList/NpArrayPageRender'
    , './functionList/NpReshapePageRender'
    , './functionList/NpZerosOnesEmptyPageRender'
    , './functionList/NpEyePageRender'
    , './functionList/NpIdentityPageRender'
    , './functionList/NpDiagPageRender'
    , './functionList/NpLinalgInvPageRender'
    , './functionList/NpFullPageRender'
    , './functionList/NpFlattenPageRender'
    , './functionList/NpFlipPageRender'
    , './functionList/NpTPageRender'
    , './functionList/NpTransposePageRender'
    , './functionList/NpSwapaxesCodeRender'
    , './functionList/NpDotPageRender'
    , './functionList/NpSumPageRender'
    , './functionList/NpConcatenatePageRender'
    , './functionList/NpDiffPageRender'
    , './functionList/NpCopyPageRender'
    , './functionList/NpLinspacePageRender'
    , './functionList/NpRavelPageRender'
    , './functionList/NpSplitPageRender'
    , './functionList/NpDsplitHsplitVsplitPageRender'
    , './functionList/NpStackPageRender'
    , './functionList/NpDstackHstackVstackPageRender'

    // , './operationList/NumpyIndexingPageRender'
    
    , './statisticsList/NpMeanVarStdMaxMinMedianPercentilePageRender'

    , './universalFunctionList/UnaryArimethicPageRender'
    , './universalFunctionList/BinaryArimethicPageRender'
    , './universalFunctionList/BinaryComparatorPageRender'
    , './universalFunctionList/UnaryLogicalPageRender'
    , './universalFunctionList/LinearAlgebraRender'
    , './universalFunctionList/NpLinalgSolveRender'
    , './universalFunctionList/TrigonometricPageRender'

    , './universalFunctionList/NpRandomRandintRender'
    , './universalFunctionList/NpRandomRandRender'
], function( requirejs, 
        NpImportRender,

        NpArangePageRender, NpArrayPageRender, NpReshapePageRender, NpZerosOnesEmptyPageRender, NpEyePageRender, 
        NpIdentityPageRender, NpDiagPageRender, NpLinalgInvPageRender, NpFullPageRender, NpFlattenPageRender, NpFlipPageRender, NpTPageRender,
        NpTransposePageRender, NpSwapaxesCodeRender, NpDotPageRender, NpSumPageRender, NpConcatenatePageRender, NpDiffPageRender, NpCopyPageRender, NpLinspacePageRender,
        NpRavelPageRender, NpSplitPageRender, NpDsplitHsplitVsplitPageRender, NpStackPageRender, NpDstackHstackVstackPageRender,


        // NumpyIndexingPageRender,
        
        NpMeanVarStdMaxMinMedianPercentilePageRender,

        UnaryArimethicPageRender, BinaryArimethicPageRender, BinaryComparatorPageRender, UnaryLogicalPageRender,
        LinearAlgebraRender, NpLinalgSolveRender, TrigonometricPageRender,

        NpRandomRandintRender,
        NpRandomRandRender
) {
    return {
        NpImportRender,

        NpArangePageRender, NpArrayPageRender, NpReshapePageRender, NpZerosOnesEmptyPageRender, NpEyePageRender, 
        NpIdentityPageRender, NpDiagPageRender, NpLinalgInvPageRender, NpFullPageRender, NpFlattenPageRender, NpFlipPageRender, NpTPageRender,
        NpTransposePageRender, NpSwapaxesCodeRender, NpDotPageRender, NpSumPageRender, NpConcatenatePageRender, NpDiffPageRender, NpCopyPageRender, NpLinspacePageRender,
        NpRavelPageRender, NpSplitPageRender, NpDsplitHsplitVsplitPageRender, NpStackPageRender, NpDstackHstackVstackPageRender,
  

        // NumpyIndexingPageRender,

        NpMeanVarStdMaxMinMedianPercentilePageRender,

        UnaryArimethicPageRender, BinaryArimethicPageRender, BinaryComparatorPageRender, UnaryLogicalPageRender,
        LinearAlgebraRender, NpLinalgSolveRender, TrigonometricPageRender,

        NpRandomRandintRender,
        NpRandomRandRender
    }
});
