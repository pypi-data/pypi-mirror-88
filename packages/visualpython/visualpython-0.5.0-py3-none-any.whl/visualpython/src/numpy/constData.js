define([

], function () {
    const STR_CHANGE_KEYUP_PASTE = 'change keyup paste';
    /**  */
    const STR_NP_ARRAY_FUNC_ID = '';
    const STR_NP_ARANGE_FUNC_ID = '';
    const STR_NP_RESHAPE_FUNC_ID = '';
    // const STR_NP_ONE_FUNC_ID = '';
    // const STR_NP_ZERO_FUNC_ID = '';

    const STR_DEPTH_KOR = '깊이';
    const STR_ROW_KOR = '행';
    const STR_COL_KOR = '열';
    const STR_INPUT_KOR = '입력';

    const STR_INPUT = 'input';
    const STR_DEPTH = 'Depth';
    const STR_ROW = 'Row';
    const STR_COL = 'Col';
    const STR_SELECTED = 'selected';

    const STR_INPUT_NUMBER = 'input number';
    const STR_INPUT_VARIABLE = 'input variable';

    const STR_INPUT_NUMBER_KOR = '숫자 입력';
    const STR_INPUT_VARIABLE_KOR = '변수 입력';

    const VP_ID_PREFIX = '#';
    const VP_CLASS_PREFIX = '.';

    /** np array */
    const STATE_paramOneArray = 'paramOneArray';
    const STATE_paramTwoArray = 'paramTwoArray';
    const STATE_paramThreeArray = 'paramThreeArray';
    const STATE_paramScalar = 'paramScalar';
    const STATE_paramVariable = 'paramVariable';

    /** np arrange */
    const STATE_paramOption1DataStart = 'paramOption1DataStart';

    const STATE_paramOption2DataStart = 'paramOption2DataStart';
    const STATE_paramOption2DataStop = 'paramOption2DataStop';

    const STATE_paramOption3DataStart = 'paramOption3DataStart';
    const STATE_paramOption3DataStop = 'paramOption3DataStop';
    const STATE_paramOption3DataStep = 'paramOption3DataStep';


    const NUMPY_HTML_URL_PATH = 'numpy/pageList/index.html';
    return {
        STR_CHANGE_KEYUP_PASTE

        , STR_DEPTH_KOR
        , STR_ROW_KOR
        , STR_COL_KOR
        , STR_INPUT_KOR
        
        , STR_INPUT
        , STR_DEPTH
        , STR_ROW
        , STR_COL
        , STR_SELECTED

        , STR_INPUT_NUMBER
        , STR_INPUT_VARIABLE

        , STR_INPUT_NUMBER_KOR
        , STR_INPUT_VARIABLE_KOR

        , VP_ID_PREFIX
        , VP_CLASS_PREFIX

        , STATE_paramOneArray
        , STATE_paramTwoArray
        , STATE_paramThreeArray
        , STATE_paramScalar
        , STATE_paramVariable

        , STATE_paramOption1DataStart

        , STATE_paramOption2DataStart
        , STATE_paramOption2DataStop
    
        , STATE_paramOption3DataStart
        , STATE_paramOption3DataStop
        , STATE_paramOption3DataStep
        
        , NUMPY_HTML_URL_PATH
    }
});
