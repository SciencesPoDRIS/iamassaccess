(function() {
    'use strict';

    /* Load modules */
    var app = angular.module('internetarchive', ['ngRoute']);

    /* Default Page Controller */
    app.controller('IAController', ['$scope',
        function($scope) {
            $scope.actions = ['create', 'update', 'delete', 'visualize'];
        }
    ]);

})();