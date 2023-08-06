define([
    './constData.js'
], function ( constData ) {
    const { API_BLOCK_PROCESS_PRODUCTION
            , API_BLOCK_PROCESS_DEVELOPMENT } = constData;
            
    const PROCESS_MODE = API_BLOCK_PROCESS_PRODUCTION;

    const API_BLOCK_VERSION_v0_1 = 0.1;
    const API_BLOCK_VERSION_v0_2 = 0.2;

    return {
        PROCESS_MODE
        , API_BLOCK_VERSION_v0_1
        , API_BLOCK_VERSION_v0_2
    }
});