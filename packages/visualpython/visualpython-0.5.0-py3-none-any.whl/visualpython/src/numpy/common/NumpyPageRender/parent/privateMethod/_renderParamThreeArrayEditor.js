define ([    
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/vpMakeDom'
    // + 추가 numpy 폴더  패키지 : 이진용 주임
    , 'nbextensions/visualpython/src/numpy/api/numpyStateApi' 
], function( vpCommon, vpMakeDom, numpyStateApi ){
    const { renderDiv, renderButton } = vpMakeDom;
    const { updateOneArrayIndexValueAndGetNewArray, 
            deleteOneArrayIndexValueAndGetNewArray,
            updateTwoArrayIndexValueAndGetNewArray,
            deleteTwoArrayIndexValueAndGetNewArray } = numpyStateApi;

    var _renderParamThreeArrayEditor = function(numpyPageRenderThis, tagSelector, stateParamName) {
        var numpyPageRenderThis = numpyPageRenderThis;
        var importPackageThis = numpyPageRenderThis.importPackageThis;
        var numpyStateGenerator = numpyPageRenderThis.numpyStateGenerator;
       
        var threeArrayDom = $(importPackageThis.wrapSelector(tagSelector));
    
        numpyPageRenderThis.resetArrayEditor(threeArrayDom);
        numpyPageRenderThis.renderParamArrayEditorTitle(threeArrayDom, tagSelector, stateParamName, 'JY903');
        /** 버튼 css 클래스 이름 중복방지 */
        // numpyPageRenderThis.renderEditorModalOpenBtn(threeArrayDom, `vp-numpy-open-threeArray-${vpCommon.getUUID()}`, 'JY903', 'column', stateParamName,tagSelector);
        
        var flexColumnDiv = renderDiv({'class':'vp-numpy-style-flex-column'});
        // 3차원 배열 렌더링
        for (var i = 0; i < numpyStateGenerator.getState(stateParamName).length; i++) {
            (function(a) {
                var threeArrayBlockDiv = renderDiv({});
                var threeArrayContainer = renderDiv({'class': 'vp-numpy-scrollbar'});
                var plusButton = renderButton({'class':'vp-numpy-func_btn'
                                                , 'style': `width: 90%; float: left; padding: 1rem;`
                                                , 'text': '+ 2 Array'});
                var deleteButton = renderButton({'class':'vp-numpy-func_btn'
                                                  , 'style': `width:10%; padding: 1rem;`
                                                  , 'text': 'x'});
                threeArrayBlockDiv.append(threeArrayContainer);
                threeArrayBlockDiv.append(plusButton);
                threeArrayBlockDiv.append(deleteButton);
        
                flexColumnDiv.append(threeArrayBlockDiv);
                threeArrayDom.append(flexColumnDiv);

                // 2차원 배열 생성
                $(plusButton).click( function() {
                    var tempNarray = [...numpyStateGenerator.getState(stateParamName)[a], ['0']];
                    numpyStateGenerator.setState({
                        [`${stateParamName}`]: updateOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), a, tempNarray)
                    });
                    numpyPageRenderThis.renderParamThreeArrayEditor(tagSelector, stateParamName);
                });

                // 3차원 배열 삭제
                $(deleteButton).click( function() {
                    var deletedParamTwoArray = deleteOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), a);
                    numpyStateGenerator.setState({
                        [`${stateParamName}`]: deletedParamTwoArray
                    });
                    numpyPageRenderThis.renderParamThreeArrayEditor(tagSelector, stateParamName);
                });
      
                //2차원 배열 렌더링
      
                for (var j = 0; j < numpyStateGenerator.getState(stateParamName)[a].length; j++) {
                    (function(b) {
                        var twoArrayBlockDiv = renderDiv({'class':`vp-numpy-style-flex-row
                                                                   vp-numpy-arrayEditor-row-block
                                                                   vp-numpy-style-margin-right-10px`});
                        var twoArrayBlockIndexDiv = renderDiv({'class':'vp-numpy-style-flex-row vp-numpy-scrollbar overflow-x-auto'
                                                                , 'style': 'width: 80%;'});
                                                    // `<div class='overflow-x-auto 
                                                    //             vp-numpy-style-flex-row 
                                                    //             vp-numpy-scrollbar' style='width: 80%;'>
                                                    //     <div class='vp-numpy-style-flex-column-center text-center' style='width: 10%;'>
                                                    //     <strong>${b} </strong>
                                                    // </div>`;
                        var twoArrayBlockIndex = renderDiv({'class': 'vp-numpy-style-flex-column-center vp-numpy-style-text-center'
                                                            ,  'style':'width: 10%;'});
                        var twoArrayRowContainerLayout = renderDiv({'class':'vp-numpy-style-flex-column'
                                                                ,'style': 'width: 90%;'}); 
                        var twoArrayRowContainer = renderDiv({'class': `vp-numpy-array-row-container vp-numpy-style-flex-row-wrap`
                                                                ,'style':'width:100%;'});
                        var plusButtonLayout = renderDiv({'class':'vp-numpy-style-flex-column-center'});
                        var plusButton = renderButton({'class': 'vp-numpy-func_btn'
                                                        , 'style': `width: 100%; height:40px; max-height:80px;`
                                                        , 'text': '+'});
                        plusButtonLayout.append(plusButton);

                        var deleteButtonLayout = renderDiv({'class': 'vp-numpy-style-flex-column-center'
                                                            , 'style':'width:10%;'});
                        var deleteButton = renderButton({'class': 'vp-numpy-func_btn'
                                                        , 'style': `width: 100%; height:40px; max-height:80px;`
                                                        , 'text': 'x'});                                      
                        deleteButtonLayout.append(deleteButton);

                        var twoArrayBlock = $(`<div class='vp-numpy-style-flex-row
                                                            vp-numpy-arrayEditor-row-block
                                                            vp-numpy-style-margin-right-10px' 
                                                    style='margin-top:5px; margin-bottom:5px;'>
                                                    <div class='overflow-x-auto 
                                                                vp-numpy-style-flex-row vp-numpy-scrollbar' style='width: 80%;'>
                                                        <div class='vp-numpy-style-flex-column-center text-center' style='width: 10%;'>
                                                            <strong>${b} </strong>
                                                        </div>     

                                                        <div class='vp-numpy-style-flex-column' style='width: 90%;'>
                                                            <div class='vp-numpy-array-row-container 
                                                                            vp-numpy-array-threeArray-row-${a}-${b}-container-${stateParamName} 
                                                                            vp-numpy-style-flex-row-wrap' style='width:100%;'>
                                                            </div>
                                                        </div>

                                                    </div>
                                                    <div class='vp-numpy-style-flex-column-center'
                                                         style='width:10%;'>
                                                        <button class='vp-numpy-func_btn 
                                                                    vp-numpy-array-threeArray-col-${a}-${b}-func-plusbtn-${stateParamName}'  
                                                                style='width: 100%; height:40px; max-height:80px;'>+</button>
                                                    </div>
                                                    <div class='vp-numpy-style-flex-column-center'
                                                         style='width:10%;'>
                                                        <button class='vp-numpy-func_btn 
                                                                   vp-numpy-array-threeArray-${a}-${b}-func-deleteBtn-${stateParamName}' 
                                                                style='width: 100%; height:40px; max-height:80px;'>x</button>
                                                    </div>
                                                </div>`);
    
                        threeArrayContainer.append(twoArrayBlock);

                        // 2차원 배열 삭제
                        $(importPackageThis.wrapSelector(`.vp-numpy-array-threeArray-${a}-${b}-func-deleteBtn-${stateParamName}`)).click( function() {
                            var deletedParamTwoArray = deleteTwoArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), a, b);
                            numpyStateGenerator.setState({
                                paramData: {
                                    [`${stateParamName}`]:deletedParamTwoArray 
                                }
                            });
                            numpyPageRenderThis.renderParamThreeArrayEditor(tagSelector, stateParamName);
                        });

                        // 1 차원 배열 생성
                        $(importPackageThis.wrapSelector(`.vp-numpy-array-threeArray-col-${a}-${b}-func-plusbtn-${stateParamName}`)).click( function() {
                         
                            var tempNarray = [...numpyStateGenerator.getState(stateParamName)[a][b], '0'];
                  
                            numpyStateGenerator.setState({
                                paramData:{
                                    [`${stateParamName}`]:  updateTwoArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), a, b, tempNarray )
                                }
                            });
                            
                            numpyPageRenderThis.renderParamThreeArrayEditor(tagSelector, stateParamName);
                        });

                        //1차원 배열 렌더링
                        for (var z = 0; z < numpyStateGenerator.getState(stateParamName)[a][b].length; z++) {
                            (function(c) {
                                var rowContainer = $(importPackageThis.wrapSelector(`.vp-numpy-array-threeArray-row-${a}-${b}-container-${stateParamName}`));
                                var colBlock = $(`<div class='flex-column'
                                                       style='margin-bottom:5px;'>
                                                    <strong>
                                                        <span class='vp-numpy-style-flex-row-center'
                                                          style='margin-top:5px;'>${c}</span>
                                                    </strong>
                                                    <input class='vp-numpy-input text-center vp-numpy-array-threeArray-${a}-${b}-${c}-input-${stateParamName}' 
                                                            value='${numpyStateGenerator.getState(stateParamName)[a][b][c]}' 
                                                            style='width:40px;' 
                                                            type='text'/>
                                                    <button class='vp-numpy-func_btn 
                                                                   vp-numpy-array-threeArray-${a}-${b}-${c}-func_deleteBtn-${stateParamName}' 
                                                            style='width:40px;'>x</button>
                                                    </div>`);
                                rowContainer.append(colBlock);


                                // 1차원 배열 행 삭제
                                $(importPackageThis.wrapSelector(`.vp-numpy-array-threeArray-${a}-${b}-${c}-func_deleteBtn-${stateParamName}`)).click( function() {
                                 
                                    var tempNarray = deleteOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName)[a][b], c);

                                    numpyStateGenerator.setState({
                                        paramData: {
                                            [`${stateParamName}`]: updateTwoArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), a, b, tempNarray )
                                        }
                                    })

                                    numpyPageRenderThis.renderParamThreeArrayEditor(tagSelector, stateParamName);
                                });
                                // 1차원 배열 행 값 변경
                                $(importPackageThis.wrapSelector(`.vp-numpy-array-threeArray-${a}-${b}-${c}-input-${stateParamName}`)).on('change keyup paste', function() {
                                    var updatedIndexValue = $(importPackageThis.wrapSelector(`.vp-numpy-array-threeArray-${a}-${b}-${c}-input-${stateParamName}`)).val();
                        
                                    var tempNarray = updateOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName)[a][b],c,updatedIndexValue);
                                
                                    numpyStateGenerator.setState({
                                        paramData:{
                                            [`${stateParamName}`]:  updateTwoArrayIndexValueAndGetNewArray(numpyStateGenerator.getState(stateParamName), a, b, tempNarray )
                                        }
                                    });
                                
                                });
                            })(z);
                        }
                    })(j);
                }
             
            })(i);
        }

        threeArrayDom.find(`.vp-numpy-array-threeArray-func_plusbtn-${stateParamName}`).off();
        threeArrayDom.find(`.vp-numpy-array-threeArray-func_plusbtn-${stateParamName}`).remove();
        
        var button = $(`<button class='vp-numpy-func_btn 
                                       vp-numpy-array-threeArray-func_plusbtn-${stateParamName}' 
                            style='width: 100%; padding: 1rem; margin-top:5px;'  >
                            <span class='vp-multilang' data-caption-id='numpyPlus3Array'>
                                + 3 Array
                            </span>
                        </button>`);
        threeArrayDom.append(button);
       

        // 3차원 배열 생성 클릭
        $(importPackageThis.wrapSelector(`.vp-numpy-array-threeArray-func_plusbtn-${stateParamName}`)).click( function() {
            numpyStateGenerator.setState({
                paramData:{
                    [`${stateParamName}`]: [...numpyStateGenerator.getState(stateParamName), [['0']]]
                }
            });
            numpyPageRenderThis.renderParamThreeArrayEditor(tagSelector, stateParamName);
        });
    }

    return _renderParamThreeArrayEditor;
});
