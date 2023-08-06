define([
    'require'
    , 'jquery'
    ,'nbextensions/visualpython/src/common/vpCommon'

    , './helperFunction'
    , './constData'
], function (requirejs, $, vpCommon,
            helperFunction, constData) {

    const { makeKernelCurrentPath } = helperFunction;
    const { NAVIGATION_DIRECTION_TYPE } = constData;
    /** 
     *  @private
     *  파이썬 커널에서
        1. 디렉토리 정보를 string으로 받아옴 
            이 함수가 디렉토리를 찾는 direction 가짓수는 총 4가지
            before 상위 디렉토리 검색
            to 특정 폴더 디렉토리 검색
            prev 이전 디렉토리 검색
            init 파일네비게이션 처음 시작할 때 기본 디렉토리 검색
        2. string을 자바스크립트 객체로 파싱
        2. 파싱된 객체정보를 <div/> 형식으로 바꿔 화면에 동적 렌더링
    */
    var _executeKernelFromDir = function(dirObj, callback, fileNavigationRendererThis) {
        const { direction } = dirObj;
        if (direction === NAVIGATION_DIRECTION_TYPE.TO || direction === NAVIGATION_DIRECTION_TYPE.PREV) {
            const { destDir } = dirObj;
            _executeCurrentPath(destDir, callback, fileNavigationRendererThis);
        } else if (direction === NAVIGATION_DIRECTION_TYPE.TOP) {
            _executeCurrentPath("..", callback, fileNavigationRendererThis);
        } else {
            _executeCurrentPath(".", callback, fileNavigationRendererThis);
        }
    }

    /**
     * @private
     * 파이썬 커널로 현재 디렉토리의 폴더 및 파일 목록 가져오기 */ 
    var _executeCurrentPath = function(path, callback, fileNavigationRendererThis) {
        var currentPathStr = makeKernelCurrentPath(path);

        fileNavigationRendererThis.vpFuncJS.kernelExecute(currentPathStr, (result) => {
            // var jsonVars = result.replace(/'/gi, `"`);
            // jsonVars = jsonVars.replace(/\\/gi, `/`);

            /** 주의 : 만약 아래의 코드 "$1"을 '$1' single quote로 바꾸면 json parsing 에러 발생 */
            var jsonVars = result.replace(/'([^']+)': /g, `"$1": `);        // 객체 앞부분 대체
            jsonVars = jsonVars.replace(/: '([^']+)'([,}])/g, `: "$1"$2`);  // 객체 뒷부분 대체
            jsonVars = jsonVars.replace(/\\/g, `/`);
            var varList = JSON.parse(jsonVars);

            /** 폴더나 파일 이름에 . 이 들어간 폴더, 파일 제거 */
            var filterd_varList = varList.filter(data => {
                if (data.name && data.name[0] == '.') {
                    return false;
                } else {
                    return true;
                }
            });
            // console.log('filterd_varList',filterd_varList);
            callback(filterd_varList);
        });
    }

    /**
     * @param {object} dirObj 
     * @param {fileNavigationRenderer This} fileNavigationRendererThis 
     */
    var executeKernelFromDir = function(dirObj, fileNavigationRendererThis) {
        fileNavigationRendererThis.startLoadingBar();
        _executeKernelFromDir(dirObj , (resultInfoArr) => {
            var { currentDirStr,  currentRelativePathStr, rootFolderName } 
                = fileNavigationRendererThis.fileNavigationState.splitPathStrAndSetStack(dirObj, resultInfoArr, 'init');
            fileNavigationRendererThis.finishLoadingBarAndSetCurrDirStr(currentDirStr, currentRelativePathStr);
            fileNavigationRendererThis.renderCurrentDirPathInfo(resultInfoArr , rootFolderName);   
        }, fileNavigationRendererThis);
    }

    /**
     * @param {object} dirObj 
     * @param {fileNavigationRenderer This} fileNavigationRendererThis 
     */
    var executeKernelFromDirBody = function(dirObj, fileNavigationRendererThis) {
        _executeKernelFromDir(dirObj , (resultInfoArr) => {
            var { currentDirStr,  currentRelativePathStr, rootFolderName } 
                = fileNavigationRendererThis.fileNavigationState.splitPathStrAndSetStack(dirObj, resultInfoArr, 'body');
            
            fileNavigationRendererThis.renderNowLocation(currentDirStr, currentRelativePathStr);
            fileNavigationRendererThis.renderCurrentDirPathInfoRightBody(resultInfoArr, rootFolderName);   
        }, fileNavigationRendererThis);
    }

    return {
       executeKernelFromDir
        , executeKernelFromDirBody
    }
});
