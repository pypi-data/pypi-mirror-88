define ([    
    // + 추가 numpy 폴더  패키지 : 이진용 주임
    'nbextensions/visualpython/src/numpy/api/numpyStateApi' 
], function( numpyStateApi ){

    var _resetArrayEditor = function(baseDom) {
        // 동적 랜더링할 태그에 css flex-column 설정
        baseDom.css('display','flex');
        baseDom.css('flexDirection','column');
        // 기존의 렌더링 태그들 리셋하고 아래 로직에서 다시 그림
        baseDom.empty()
    }
    return _resetArrayEditor;
});
