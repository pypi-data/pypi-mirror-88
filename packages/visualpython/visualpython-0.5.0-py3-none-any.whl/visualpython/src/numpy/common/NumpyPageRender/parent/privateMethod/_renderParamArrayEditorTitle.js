define ([    
    'nbextensions/visualpython/src/common/vpCommon'
    // + 추가 numpy 폴더  패키지 : 이진용 주임
    , 'nbextensions/visualpython/src/numpy/api/numpyStateApi' 
], function( vpCommon, numpyStateApi ){
    /**
     * oneArrayEditor twoArrayEditor threeArrayEditor의 제목과 생성 버튼, 크게보기 버튼을 렌더링하는 메소드
     * @param {numpyPageRender This} numpyPageRenderThis 
     * @param {document} baseDom 
     * @param {string} tagSelector 
     * @param {string} stateParamName 
     * @param {string} funcId 
     */
    var _renderParamArrayEditorTitle = function(numpyPageRenderThis, baseDom, tagSelector, stateParamName, funcId) {
        var numpyPageRenderThis = numpyPageRenderThis;
        var importPackageThis = numpyPageRenderThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRenderThis.getStateGenerator();
        var uuid = vpCommon.getUUID();
        var dom;
        switch(funcId){
            /**
             * oneArrayEditor
             */
            case 'JY901':{
                /** 1차원 배열 행의 길이를 구하는 로직 */
                numpyPageRenderThis.setOneArrayLength ( numpyStateGenerator.getState(stateParamName).length );
                
                /** 1차원 배열 길이 값 입력 <div>블럭 생성 */
                dom = $(`<div class='vp-numpy-style-flex-row-center' style='margin-bottom:5px;'>
                                <div style='margin:0 5px;'>
                                    <span class='vp-multilang' data-caption-id='length-kor'>Length : </span>
                                    <input class='vp-numpy-input
                                                  vp-numpy-oneArrayEditor-length-input 
                                                  vp-numpy-oneArrayEditor-length-input-${uuid}'

                                        value='${numpyPageRenderThis.getOneArrayLength()}' 
                                        type='text'/>
                                </div>
                                <button class='vp-numpy-func_btn vp-numpy-oneArrayEditor-make-btn-${uuid}'>New</button>
                            </div>`);
                baseDom.append(dom);

                /**  1차원 배열 길이를 입력하는 이벤트 함수  */
                $(importPackageThis.wrapSelector(`.vp-numpy-oneArrayEditor-length-input-${uuid}`)).on('change keyup paste', function() {
                    numpyPageRenderThis.setOneArrayLength ( parseInt($(this).val()) );
                });

                /**  입력한 길이 숫자 만큼의 1차원 배열을 생성하는 이벤트 함수  */
                $(importPackageThis.wrapSelector(`.vp-numpy-oneArrayEditor-make-btn-${uuid}`)).click(function() {
                    var newArray = [];
                    for(var i = 0; i <  numpyPageRenderThis.getOneArrayLength(); i++){
                        newArray.push('0');
                    }
                    numpyStateGenerator.setState({
                        paramData: {
                            [`${stateParamName}`]: newArray
                        }
                    });
                    numpyPageRenderThis.renderParamOneArrayEditor(tagSelector, stateParamName);
                });
                break;
            }
            /**
             * twoArrayEditor
             */
            case 'JY902':{
                /** 2차원 배열 행의 길이를 구하는 로직 */
                numpyPageRenderThis.setTwoArrayRow(numpyStateGenerator.getState(stateParamName).length);

                /** 2차원 배열 열의 길이를 구하는 로직 */
                var maxColNum = 0;
                numpyStateGenerator.getState(stateParamName).forEach(elementArray => {
                    var num = elementArray.length;
                    maxColNum = Math.max(maxColNum, num);
                });
                numpyPageRenderThis.setTwoArrayCol(maxColNum);

                /** 2차원 행 열 값 입력 <div>블럭 생성 */
                dom = $(`<div class='vp-numpy-style-flex-row-center' style='margin-bottom:5px;'>
                            <div style='margin:0 5px;'>
                                <span  class='vp-multilang' data-caption-id='row-kor'>Row : </span>
                                <input class='vp-numpy-input
                                              vp-numpy-twoArrayEditor-row-input
                                              vp-numpy-twoArrayEditor-row-input-${uuid}'
                                    value='${numpyPageRenderThis.getTwoArrayRow()}'
                                    type='text'/>
                            </div>
                            <div style='margin:0 5px;'>
                                <span  class='vp-multilang' data-caption-id='col-kor'>Col : </span>
                                <input class='vp-numpy-input 
                                              vp-numpy-twoArrayEditor-col-input 
                                              vp-numpy-twoArrayEditor-col-input-${uuid}' 
                                    value='${numpyPageRenderThis.getTwoArrayCol()}'
                                    type='text'/>
                            </div>
                                <button class='vp-numpy-func_btn vp-numpy-twoArrayEditor-make-btn-${uuid}'>New</button>
                            </div>`);
                baseDom.append(dom);

                /** 2차원 배열 행의 길이 값을 입력하는 이벤트 함수 */
                $(importPackageThis.wrapSelector(`.vp-numpy-twoArrayEditor-row-input-${uuid}`)).on('change keyup paste', function() {
                    numpyPageRenderThis.setTwoArrayRow( parseInt( $(this).val() ) );
                });
                /** 2차원 배열 열의 길이 값을 입력하는 이벤트 함수 */
                $(importPackageThis.wrapSelector(`.vp-numpy-twoArrayEditor-col-input-${uuid}`)).on('change keyup paste', function() {
                    numpyPageRenderThis.setTwoArrayCol( parseInt( $(this).val() ) );
                });

                /** 입력한 행과 열의 숫자 만큼의 2차원 배열 을 생성하는 이벤트 함수 */
                $(importPackageThis.wrapSelector(`.vp-numpy-twoArrayEditor-make-btn-${uuid}`)).click(function() {
                    var newTwoArray = [];
                    for(var i = 0; i < numpyPageRenderThis.getTwoArrayRow(); i++){
                        newTwoArray.push([]);
                        for(var j = 0; j < numpyPageRenderThis.getTwoArrayCol(); j++){
                            newTwoArray[i].push('0');
                        }
                    }
                    numpyStateGenerator.setState({
                        paramData: {
                            [`${stateParamName}`]: newTwoArray
                        }
                    });

                    /** 2차원 배열 생성 버튼을 클릭하면 입력한 행과 열의 숫자 만큼의 2차원 배열을 다시 렌더링 */
                    numpyPageRenderThis.renderParamTwoArrayEditor(tagSelector, stateParamName);
                });

                break;
            }
            /**
             * threeArrayEditor
             */
            case 'JY903':{
                /** 3차원 배열 면(깊이) 행 열의 길이를 구하는 로직 */
                numpyPageRenderThis.setThreeArrayDepth(numpyStateGenerator.getState(stateParamName).length);
                var maxRowNum = 0;
                var maxColNum = 0;
                numpyStateGenerator.getState(stateParamName).forEach(elementArray => {
                    var num = elementArray.length;
                    maxRowNum = Math.max(maxRowNum, num);
                    elementArray.forEach(innerArray => {
                        var num2 = innerArray.length;
                        maxColNum = Math.max(maxColNum, num2);
                    });
                });
                numpyPageRenderThis.setThreeArrayRow( maxRowNum );
                numpyPageRenderThis.setThreeArrayCol( maxColNum );

                /** 3차원 행 열 값 입력 <div>블럭 생성 
                  */
                dom = $(`<div class='vp-numpy-style-flex-row-center' style='margin-bottom:5px;'>
                            <div style='margin:0 5px;'>
                                <span  class='vp-multilang' data-caption-id='depth-kor'>Depth : </span>
                                <input class='vp-numpy-input 
                                              vp-numpy-threeArrayEditor-depth-input 
                                              vp-numpy-threeArrayEditor-depth-input-${uuid}' 
                                    value='${numpyPageRenderThis.getThreeArrayDepth()}'
                                    type='text'/>
                            </div>
                            <div style='margin:0 5px;'>
                                <span  class='vp-multilang' data-caption-id='row-kor'>Row : </span>
                                <input class='vp-numpy-input
                                              vp-numpy-threeArrayEditor-row-input 
                                              vp-numpy-threeArrayEditor-row-input-${uuid}' 
                                    value='${numpyPageRenderThis.getThreeArrayRow()}'
                                    type='text'/>
                            </div>
                            <div style='margin:0 5px;'>
                                <span  class='vp-multilang' data-caption-id='col-kor'>Col : </span>
                                <input class='vp-numpy-input 
                                              vp-numpy-threeArrayEditor-col-input 
                                              vp-numpy-threeArrayEditor-col-input-${uuid}' 
                                    value='${numpyPageRenderThis.getThreeArrayCol()}'
                                    type='text'/>
                            </div>
                                <button class='vp-numpy-func_btn vp-numpy-threeArrayEditor-make-btn-${uuid}'>New</button>
                            </div>`);
                baseDom.append(dom);

                /** 3차원 배열 행의 길이 값을 입력하는 이벤트 함수 */
                $(importPackageThis.wrapSelector(`.vp-numpy-threeArrayEditor-row-input-${uuid}`)).on('change keyup paste', function() {
                    numpyPageRenderThis.setThreeArrayRow( parseInt($(this).val()) );
                });

                /** 3차원 배열 열의 길이 값을 입력하는 이벤트 함수 */
                $(importPackageThis.wrapSelector(`.vp-numpy-threeArrayEditor-col-input-${uuid}`)).on('change keyup paste', function() {
                    numpyPageRenderThis.setThreeArrayCol( parseInt($(this).val()) );
                });   

                 /** 3차원 배열 깊이의 길이 값을 입력하는 이벤트 함수 */
                $(importPackageThis.wrapSelector(`.vp-numpy-threeArrayEditor-depth-input-${uuid}`)).on('change keyup paste', function() {
                    numpyPageRenderThis.setThreeArrayDepth( parseInt($(this).val()) );
                });        

                /**
                 * 3차원 배열을 생성하는 이벤트 함수
                 */
                $(importPackageThis.wrapSelector(`.vp-numpy-threeArrayEditor-make-btn-${uuid}`)).click(function() {
                    var newThreeArray = [];
                    for(var i = 0; i < numpyPageRenderThis.getThreeArrayDepth(); i++) {
                        newThreeArray.push([]); 
                        for(var j = 0; j < numpyPageRenderThis.getThreeArrayRow(); j++) {
                            newThreeArray[i].push([]);
                            for(var z = 0; z < numpyPageRenderThis.getThreeArrayCol(); z++) {
                                newThreeArray[i][j].push('0');
                            }
                        }
                    }
                    numpyStateGenerator.setState({
                        paramData: {
                            [`${stateParamName}`]: newThreeArray
                        }
                    });
                    numpyPageRenderThis.renderParamThreeArrayEditor(tagSelector, stateParamName);
                });
                break;
            }
        }
    }

    return _renderParamArrayEditorTitle;
});
