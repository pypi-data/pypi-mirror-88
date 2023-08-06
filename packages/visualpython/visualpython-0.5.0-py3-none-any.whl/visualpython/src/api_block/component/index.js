define([
    './option/class_option.js'
  , './option/def_option.js'
  , './option/if_option.js'    
  , './option/elif_option.js'  
  , './option/else_option.js'  

  , './option/for_option.js' 
  , './option/listfor_option.js' 
  , './option/try_option.js' 
  , './option/import_option.js'   
  , './option/lambda_option.js'
  , './option/while_option.js'
  , './option/try_option.js'
  , './option/except_option.js'

  , './option/code_option.js'
  , './option/break_option.js'
  , './option/continue_option.js'
  , './option/pass_option.js'
  , './option/property_option.js'
  , './option/comment_option.js'
  , './option/return_option.js'

  , './boardMenuBar.js'
  , './option/sample_option.js'
  , './option/api_option.js'
], function ( InitClassBlockOption
            , InitDefBlockOption 
            , InitIfBlockOption
            , InitElifBlockOption
            , InitElseBlockOption

            , InitForBlockOption
            , InitListForBlockOption
            , InitTryBlockOption
            , InitImportBlockOption
            , InitLambdaBlockOption
            , InitWhileBlockOption
            , InitTryBlockOption
            , InitExceptBlockOption

            , InitCodeBlockOption
            , InitReturnBlockOption

            , InitBoardMenuBar
            , InitSampleBlockOption
            , InitApiBlockOption  ) {

  return {
      InitClassBlockOption
      , InitDefBlockOption 
      , InitIfBlockOption
      , InitElifBlockOption
      , InitElseBlockOption
      
      , InitForBlockOption
      , InitListForBlockOption
      , InitTryBlockOption
      , InitImportBlockOption
      , InitLambdaBlockOption
      , InitWhileBlockOption
      , InitTryBlockOption
      , InitExceptBlockOption

      , InitCodeBlockOption
      , InitReturnBlockOption

      , InitBoardMenuBar
      , InitSampleBlockOption
      , InitApiBlockOption
  }
});
