define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/vpMakeDom'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    //
    , 'nbextensions/visualpython/src/component/fileNavigation/api'
    , 'nbextensions/visualpython/src/component/fileNavigation/executor'
    , 'nbextensions/visualpython/src/component/fileNavigation/constData'
], function ( requirejs, $, vpCommon, vpMakeDom, sb,
              componentConstApi, executor, constData) {

    const { NAVIGATION_DIRECTION_TYPE } = constData;
    // kernel executor에 필요한 함수 import
    const { executeKernelFromDir,
            executeKernelFromDirBody } = executor;
    // dom 만드는데 필요한 함수 import
    const { controlToggleInput } = componentConstApi;
    const { renderSpan, renderLi } = vpMakeDom;
    // stringBuilder import
    // var sbCode = new sb.StringBuilder();

    var FileNavigationRenderer = function(fileNavigationState, vpFuncJS, fileResultState) {
        this.fileNavigationState = fileNavigationState;
        this.vpFuncJS = vpFuncJS;
        this.fileResultState = fileResultState;
    }

    FileNavigationRenderer.prototype.getFileNavigationState = function() {
        return this.fileNavigationState;
    }

    // CSV 파일네비게이션 시작시 처음으로 렌더링하는 함수
    FileNavigationRenderer.prototype.initRender = function() {
        var fileNavigationRendererThis = this;
        var dirObj = {
            direction: NAVIGATION_DIRECTION_TYPE.INIT,
        }
 
        executeKernelFromDir(dirObj, fileNavigationRendererThis);

        /** fileNavigation right tab에 현재 path의 폴더와 파일들 렌더링 */
        executeKernelFromDirBody(dirObj, fileNavigationRendererThis);

        /** 만약 타입이 'SAVE_FILE'일 경우' */
        var fileNavigationState = fileNavigationRendererThis.getFileNavigationState();
        var fileNavigationtype = fileNavigationState.getFileNavigationtype();
        var fileOptionData = fileNavigationState.getFileOptionData();

        /** Pandas > File IO > to_csv(), to_excel(), to_json(), to_pickle() 네비게이션 클릭시 */
        if(fileNavigationtype === 'SAVE_FILE'){

            /** 20201118 이진용 주임 수정 */
            /** 현재 디렉토리에 파일 저장 -> Save file to current directory */
            /** 파일 이름 입력 -> Input file name */
            var saveFileDataBtn = $(`<button class='directoryComponent-btn-saveVisualPython'
                                                 style='margin-left: 10px;'>Save file to current directory</button>`);
            var saveFileDataInput = $(`<input id='vp-fileNavigation' type='text' placeholder='Input file name'></input>`);
            $('.directoryComponent-savebutton').append(saveFileDataInput);
            $('.directoryComponent-savebutton').append(saveFileDataBtn);
         
            controlToggleInput();
            $(saveFileDataInput).on('change keyup paste', function() {
                fileNavigationState.setVisualPythonFileName($(this).val());
            });
            
            /** 
             * 현재 디렉토리에 저장 버튼을 누르면 실행되는 이벤트 click 함수 
             */
            $(saveFileDataBtn).click(function(){
                if(fileNavigationState.getVisualPythonFileName() === ``){
                    /** 20201118 이진용 주임 수정 */
                    /** File 이름을 입력해주세요 -> Please input file name */
                    vpCommon.renderAlertModal('Please input file name');
                    return;
                }
                var dirPath = fileNavigationRendererThis.makeNewCurrRelativePath();

                var fileName = `${fileNavigationState.getVisualPythonFileName()}`;
                if (fileName.indexOf('.' + fileOptionData.fileExtension) === -1) {
                    fileName += `.${fileOptionData.fileExtension}`;
                }

                fileNavigationRendererThis.selectFile(dirPath, fileName);
                fileNavigationState.resetStack();
            });
        }
    }

    /** */
    FileNavigationRenderer.prototype.renderCurrentDirPathInfo = function(dirInfoArr, rootFolderName) {
        $('.directoryComponent-container').empty();

        var currentDirRootDom = $(`<div class='directoryComponent-right vp-scrollbar'>
                                  </div>`);
        var { folderArr } = this.makeFolderOrFileDomArr(dirInfoArr);
    
        currentDirRootDom.appendTo('.directoryComponent-container');
        var directoryComponentUl = $('.directoryComponent-ul');
        folderArr.forEach(dom => {
            directoryComponentUl.append(dom);
        });
    }

    /** */
    FileNavigationRenderer.prototype.renderCurrentDirPathInfoRightBody = function(dirInfoArr, rootFolderName) {
        $('.directoryComponent-right').empty();
        var currentDirRootDom = $(`<div class='directoryComponent-body'></div>`);
        var { folderArr, fileArr } = this.makeFolderOrFileDomArr(dirInfoArr);
        
        var directoryComponentUl = $(`<ul class='directoryComponent-ul'>
                                      </ul>`);
  
        folderArr.forEach(dom => {
            directoryComponentUl.append(dom);
        });
        fileArr.forEach(dom => {
            directoryComponentUl.append(dom);
        });
        currentDirRootDom.append(directoryComponentUl);
        currentDirRootDom.appendTo('.directoryComponent-right');
    }

    /** <div/> 태그 형식의 폴더 디렉토리를 만드는 함수 */
    FileNavigationRenderer.prototype.makeFolderDom = function(node) {
        var fileNavigationRendererThis = this;

        var folderName = node.name;
        var folderPath = node.path;

        var directoryLi = renderLi({class: 'directoryComponent-li'});
        var directorySpan = renderSpan({class:'directoryComponent-column'});
        // var directorySpanDir = renderSpan({class:'directoryComponent-dir-text icon-folder'
        //                                     ,text: `${folderName}`});
        var directorySpanDir = $(`<i class="directoryComponent-dir-text item_icon folder_icon icon-fixed-width">
                                            ${folderName}
                                            </i>`);
        $(directorySpanDir).click(function() {
            var dirObj = {
                direction: NAVIGATION_DIRECTION_TYPE.TO,
                destDir: folderPath
            }
            executeKernelFromDirBody(dirObj, fileNavigationRendererThis);
        });

        $(directoryLi).append($(directorySpan).append(directorySpanDir));
        return directoryLi;
    }

    /**  <div/> 태그 형식의 파일 디렉토리를 만드는 함수 */
    FileNavigationRenderer.prototype.makeFileDom = function(node) {
        var that = this;
        var fileNavigationState = this.getFileNavigationState();
        var fileName = node.name;

        var directoryLi = renderLi({class: 'directoryComponent-li'});
        // var directorySpan = renderSpan({class: 'directoryComponent-column directoryComponent-dir-text icon-file'
        //                                , text: `${fileName}`});
        var directorySpan = $(`<i class="directoryComponent-dir-text item_icon file_icon icon-fixed-width">
                                       ${fileName}
                                       </i>`);
        directorySpan.click(function() {
            var dirPath = that.makeNewCurrRelativePath();
            var dataOption = fileNavigationState.getFileOptionData();
            if (fileName.indexOf('.' + dataOption.fileExtension) === -1) {
                vpCommon.renderAlertModal('Not ' + dataOption.fileExtension + ' file');
                return;
            }

            that.selectFile(dirPath, fileName);
        });

        directoryLi.append(directorySpan);
        return directoryLi;
    }

    
    FileNavigationRenderer.prototype.makeFolderOrFileDomArr = function(dirInfoArr) {
        var fileNavigationRendererThis = this;

        var folderArr = [];
        var fileArr = [];

        var nodeInfo = { name:'', 
                         type:'' };
        // 디렉토리 정보가 담긴 자바스크립트 배열 dirInfoArr을 index 1부터 1씩 늘려가면서
        // 폴더인지 파일인지 확인후 html 태그를 만든다. 
        // index 0의 데이터는 현재 디렉토리가 담긴 별도의 특수 데이터라 건너 뛴다.
        var index = 1;
        while(index < dirInfoArr.length) {
            nodeInfo = dirInfoArr[index];
            var tempDom = null;
            // 디렉토리 정보가 폴더 일 경우
            if (nodeInfo.type === 'dir') {
                tempDom = fileNavigationRendererThis.makeFolderDom(nodeInfo);
                folderArr.push(tempDom);
            } else {
            // 디렉토리 정보가 파일 일 경우
                tempDom = fileNavigationRendererThis.makeFileDom(nodeInfo);
                fileArr.push(tempDom);
            }

            index++;
        }

        return {
            folderArr, fileArr
        }
    }

    FileNavigationRenderer.prototype.makeNewCurrRelativePath = function() {
        var fileNavigationState = this.getFileNavigationState();
        var dirPath = fileNavigationState.getRelativeDir();
        /** 
         *  만약 현재 전체 path가 C:/Users/L.E.E/Desktop/Bit Python이라면,
         *  baseFolder 변수에 Bit Python가 저장됨
         *  즉 파일 네비게이션을 연 시점의 폴더가 baseFolder 
         */
        var baseFolder = fileNavigationState.getBaseFolder();
        /** 
         *  만약 현재 전체 path가 C:/Users/L.E.E/Desktop/Bit Python이라면,
         *  Jupyter.notebook.notebook_path 는 'Desktop/Bit Python/Untitled4.ipynb' 
         *  noteBookFolder 변수에 Desktop가 저장됨
         *  즉 Jupyter.notebook.notebook_path의 폴더가 noteBookFolder
         */
        var noteBookFolder = fileNavigationState.getNotebookFolder();


        /** 파일 네비게이션을 실행한 baseFolder 이름이 현재 상대 경로에 있을때 */
        if (dirPath.indexOf(baseFolder) !== -1) {
            var baseFolderIndex = dirPath.indexOf(baseFolder);
            dirPath = dirPath.substring(baseFolderIndex,dirPath.length);
            dirPath = dirPath.replace(baseFolder, '');
        }
        
        /** 만약 baseFolder 이름과 noteBookFolder 이름이 동일하면 
         *  dirPath 안에 존재하는 noteBookFolder이름을  replace 하지 않음
         * */
        if (baseFolder !== noteBookFolder) {
            dirPath = dirPath.replace(noteBookFolder, '');
        }

        if (dirPath[0] === '/') {
            dirPath = dirPath.substring(1, dirPath.length);
        }
        return dirPath;
    }

    // loadingBar를 생성합니다.
    FileNavigationRenderer.prototype.startLoadingBar = function() {
        $('.directoryComponent-container').empty();
        this.renderLoadingBar();
    }

    // loadingBar를 종료합니다.
    FileNavigationRenderer.prototype.finishLoadingBarAndSetCurrDirStr = function(currentDirStr, currentRelativePathStr) {
        var fileNavigationRendererThis = this;
        fileNavigationRendererThis.fileNavigationState.setRelativeDir(currentRelativePathStr);
        fileNavigationRendererThis.fileNavigationState.setCurrentDir(currentDirStr);

        $('.directoryComponent-container').find('#vp_loadingBar').remove();
    }

    // 로딩을 생성하는 함수
    FileNavigationRenderer.prototype.renderLoadingBar = function() {
        vpCommon.renderLoadingBar();
    }

    /** */
    FileNavigationRenderer.prototype.renderNowLocation = function(currentDirStr, currentRelativePathStr) {
        /** 이 메소드에서 사용할 state 데이터 가져오기 */
        var fileNavigationRendererThis = this;
        var fileNavigationState = this.getFileNavigationState();
        fileNavigationState.setRelativeDir(currentRelativePathStr);
        fileNavigationState.setCurrentDir(currentDirStr);

        var notebookPathStr = fileNavigationState.getNotebookDir();
        var notebookPathStrLength = notebookPathStr.length;
        var baseFolder = fileNavigationState.getBaseFolder();
        var notebookFolder = fileNavigationState.getNotebookFolder();
        /** 파일 네비게이션에 현재 path를 렌더링해서 보여주는 logic */
        var currentRelativePathStrArray = currentRelativePathStr.split('/');
        
        if (baseFolder === notebookFolder && Jupyter.notebook.notebook_path.indexOf('/') === -1) {
            var index = currentRelativePathStrArray.indexOf(baseFolder)
            currentRelativePathStrArray.splice(index,1);
        }

        var currentRelativePathDomElement = $(`<div><div>`);
        var basePathDomElement = $(`<span class='vp-filenavigation-nowLocation' value='/'> / </span>`);
        currentRelativePathDomElement.append(basePathDomElement);
        basePathDomElement.click(function() {
            var dirObj = {
                direction: NAVIGATION_DIRECTION_TYPE.TO,
                destDir: notebookPathStr
            }
            // fileNavigation body에 현재 path의 폴더와 파일들 렌더링
            executeKernelFromDirBody(dirObj, fileNavigationRendererThis);
        });

        var nestedLength = 0;
        currentRelativePathStrArray.forEach((pathToken,index) => {
            if (index === 0) {
                slashStr = '';
            } else {
                slashStr = '/';
            }

            var spanElement = $(`<span class='vp-filenavigation-nowLocation' value='${pathToken}'> ${slashStr} ${pathToken} </span>`);
            var pathLength = notebookPathStrLength + pathToken.length + 1 + nestedLength;
            spanElement.click(function() {
                var currentRelativePathStr = `${currentDirStr.substring(0, pathLength)}`;
     
                var dirObj = {
                    direction: NAVIGATION_DIRECTION_TYPE.TO,
                    destDir: currentRelativePathStr
                }
             
                // fileNavigation body에 현재 path의 폴더와 파일들 렌더링
                executeKernelFromDirBody(dirObj, fileNavigationRendererThis);
                
            });
            currentRelativePathDomElement.append(spanElement);
            nestedLength += pathToken.length + 1;
        });
             
        $('.directoryComponent-directory-nowLocation').empty();
        $('.directoryComponent-directory-nowLocation').append(currentRelativePathDomElement);
    }

    FileNavigationRenderer.prototype.selectFile = function(relativeDirPath, filePathStr) {
        var fileNavigationRendererThis = this;
        var fileNavigationState = fileNavigationRendererThis.getFileNavigationState();

        /** 상대 경로 string을 자르고 붙이는 로직 */
        var baseFolder = fileNavigationState.getBaseFolder();
        var baseDirStr = fileNavigationState.getBaseDir();
        var noteBookPathStr = fileNavigationState.getNotebookDir();
        var currentDirStr = fileNavigationState.getCurrentDir();
        var noteBookPathStrLength = noteBookPathStr.length;
       
        var baseDirStrLength = baseDirStr.length;

        /** upDirectoryCount는 파일 네비게이션을 연 시점의 path 경로 에서 
         *  얼마만큼 상위 path로 올라갔는지 횟수를 count하는 변수 
         */
        var upDirectoryCount = 0;
        var _upDirectoryCount = 0;

        var splitedNoteBookPathStrArray = noteBookPathStr.split('/');
        var splitedBaseDirArray = baseDirStr.split('/');
        var splitedCurrentDirArray  = currentDirStr.split('/');

        var relativeBaseDirArray = splitedBaseDirArray.slice(splitedNoteBookPathStrArray.length, splitedBaseDirArray.length);
        var relativeCurrentDirArray = splitedCurrentDirArray.slice(splitedNoteBookPathStrArray.length, splitedCurrentDirArray.length);

        /** 최초 파일 네비게이션을 연 시점의 path 경로와 Jupyter notebook의 path 경로를 비교하여
         *  최초 파일 네비게이션을 연 시점의 path에서 얼마만큼 상위로 올라가야 Jupyter notebook의 path 경로에 도달할 수 있는지 count
         */
        var _baseDirStrLength = baseDirStrLength;
        while ( noteBookPathStrLength < _baseDirStrLength ) {
            _baseDirStrLength--;
            if ( baseDirStr[_baseDirStrLength] === '/') {
                upDirectoryCount += 1;
            }
        }

        /** Jupyter notebook의 path 경로와 현재 이동한 path 경로를 비교하여
         *  Jupyter notebook의 path 경로에서 얼마만큼 하위로 내려와야 현재 이동한 path 경로에 도달할 수 있는지 count
         */
        relativeCurrentDirArray.forEach((forderName,index) => {
            if ( forderName === relativeBaseDirArray[index] ) {
                upDirectoryCount -= 1;
            }
        });
       
        /**upDirectoryCount의 숫자 만큼 '../'을 추가
         * upDirectoryCount의 숫자 만큼 다시말하면 '../'가 추가 된 만큼, 현재 path 폴더에서 상위 폴더로 이동했다는 의미.
         */
        _upDirectoryCount = upDirectoryCount;
        var prefixUpDirectory = ``;
        while (_upDirectoryCount-- > 0) {
            prefixUpDirectory += `../`;
        }

        var slashstr = `/`;
        if (relativeDirPath === '') {
            slashstr = '';
        }

        /** 최초의 path가 C:/Users/L.E.E/Desktop/Bit Python이라면, baseFolder는 Bit Python
         *  현재 이동한 시점의 path에서 baseFolder인 Bit Python가 존재하지 않을 때
         */
        if (upDirectoryCount > 0 && currentDirStr.indexOf(baseFolder) === -1) {
            $(fileNavigationRendererThis.fileResultState.pathInputId).val(`${prefixUpDirectory}${relativeDirPath}${slashstr}${filePathStr}`);
            $(fileNavigationRendererThis.fileResultState.fileInputId).val(`${filePathStr}`);
        /** 현재 이동한 시점의 path에서 baseFolder인 Bit Python가 존재할 때 */
        } else {
            $(fileNavigationRendererThis.fileResultState.pathInputId).val(`./${relativeDirPath}${slashstr}${filePathStr}`);
            $(fileNavigationRendererThis.fileResultState.fileInputId).val(`${filePathStr}`);
        }

        vpCommon.renderSuccessMessage(`${filePathStr} selection completed`);
        /** 장안태 추가. 파일 선택 완료시 문서 이벤트 발동 */
        if (fileNavigationState.getFileNavigationtype() === 'SAVE_FILE') {
            $(document).trigger({
                type:"fileSaveSelected.fileNavigation",
                path:`${filePathStr}`
            });
        } else {
            $(document).trigger({
                type:"fileReadSelected.fileNavigation",
                path:`${filePathStr}`
            });
        }
   
        $('#vp_fileNavigation').addClass('hide');
        $('#vp_fileNavigation').removeClass('show');
        $('#vp_fileNavigation').remove();
        
        // 파일 네비게이션에서 생성된 script 파일 삭제
        vpCommon.removeHeadScript('fileNavigation');
        vpCommon.removeHeadScript('loadingBar');
    }

    return FileNavigationRenderer;
});
