(function() {
    'use strict';

    /* Load modules */
    var app = angular.module('internetarchive', ['ngRoute']);

    /* Default Page Controller */
    app.controller('IAController', ['$scope', '$http',
        function($scope, $http) {
            $scope.actions = ['create', 'update', 'delete', 'visualize'];

            $scope.submit = function() {
                if ($scope.action === undefined) {
                    alert('Please choose an action to process !');
                } else {
                    $http.get('http://localhost:5000/create').success(function(data, status, headers, config) {
                        console.log(data);
                    }).error(function(data, status, headers, config) {
                        console.log('Error');
                        console.log(arguments);
                    });
                }
            }
        }
    ]);

})();