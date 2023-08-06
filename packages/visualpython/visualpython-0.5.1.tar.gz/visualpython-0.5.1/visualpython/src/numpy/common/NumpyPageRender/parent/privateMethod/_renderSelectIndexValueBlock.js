define ([    
    'nbextensions/visualpython/src/common/vpCommon'
], function( vpCommon ) {

    /** numpy의 기타 indexValue 옵션을 Select하는 블록을 렌더링하는 함수
     * @param {numpyPageRenderer this} numpyPageRendererThis 
     * @param {string} title 
     * @param {string || Array<string> || Array<object>} stateParamNameOrSelectValueDataArray 
     *      if {string} stateParamName
     *      else {Array<object>} SelectValueDataArray 
     */
    var _renderSelectIndexValueBlock = function(numpyPageRendererThis, title, stateParamNameOrSelectValueDataArray) {
        var uuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();
        var optionPageSelector = numpyPageRendererThis.getOptionPageSelector();
        var optionPage = $(importPackageThis.wrapSelector(optionPageSelector));

        var numpyIndexValueArray = numpyPageRendererThis.numpyIndexValueArray;
        var indexBlock = $(`<tr class='vp-numpy-option-block 
                                        vp-numpy-${uuid}-block' 
                                id='vp_blockArea'>

                            </tr>`);
                 
        optionPage.append(indexBlock);
        // var numpyBlock = $(importPackageThis.wrapSelector(`.vp-numpy-${uuid}-block`));
        // var flexRow = $(`<div class='vp-numpy-style-flex-row'></div>`);
        // numpyBlock.append(flexRow);

        /**
         *  파라미터 타입에 따라 처리하는 경우의 수가 달라진다.
         */
        if(Array.isArray(stateParamNameOrSelectValueDataArray)){
            /**
             * SelectValueDataArray의 경우 데이터 안에
             * stateParamName, selectParamName, optionDataList 값을 가지고 있다.
             * stateParamName은 입력 받을 state 이름
             * selectParamName은 <span>태그에 렌더링할 이름
             * optionDataList는 유저가 select해서 선택할 수 있는 numpy 함수 옵션 값 목록 
             */ 
                                
            for(var i = 0; i < stateParamNameOrSelectValueDataArray.length; i++){
                (function(j) {
                    var uuid2 = vpCommon.getUUID();
                    var numpySelect = $(` 
                                                <td>
                                                    ${title}
                                                </td>
                                                    
                                                <td>
                                                    <select class='vp-numpy-select-${uuid2}' 
                                                            id='vp_numpySelect'></select>
                                                </td>
                                            `);
                    indexBlock.append(numpySelect);

                    /**
                     *  select 태그 배열에 옵션 데이터 리스트를 <option>태그에 담아 렌더링한다
                     */
                    stateParamNameOrSelectValueDataArray[j].optionDataList.forEach((element) => {
                        $(importPackageThis.wrapSelector(`.vp-numpy-select-${uuid2}`)).append(`<option value='${element}'> ${element}</option>`)
                    });
                    
                    /**
                     *  옵션 select 해서 입력받을 수 있는 state를 change하는 이벤트 함수를 bind 한다
                     */
                    $(importPackageThis.wrapSelector(`.vp-numpy-select-${uuid2}`)).change(function() {
                        numpyStateGenerator.setState({
                            [`${stateParamNameOrSelectValueDataArray[j].stateParamName}`]: $(':selected', this).val()
                        });
                    });
                })(i);
            }
        } else {    
            /**
             *  stateParamName일 경우
             */

            /**
             *  select 태그에 옵션 데이터 리스트를 <option>태그에 담아 렌더링한다
            */
                                        
            var numpySelect = $(`
                                        <th>
                                            ${title}
                                        </th>
                                            
                                        <td>
                                            <select class='vp-numpy-select' id='vp_numpySelect'></select>
                                        </td>
                                    `);
            indexBlock.append(numpySelect);
            numpyIndexValueArray.forEach((element) => {
                $(importPackageThis.wrapSelector('#vp_numpySelect')).append(`<option value='${element}'> ${element}</option>`)
            });

           /**
            *  옵션 select 해서 입력받을 수 있는 state를 change하는 이벤트 함수를 bind 한다
            */
            $(importPackageThis.wrapSelector('#vp_numpySelect')).change(function() {
                var stateParamName = stateParamNameOrSelectValueDataArray;
                numpyStateGenerator.setState({
                    [`${stateParamName}`]: $(':selected', this).val()
                });
            });
        }
    }
    
    return  _renderSelectIndexValueBlock;

});
