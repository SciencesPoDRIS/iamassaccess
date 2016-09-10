(function() {
    'use strict';

    var app = angular.module("iamassaccess", ['ngMaterial', 'ngCsvImport', 'myapp.directives', 'ngTable', 'ngFileUpload']);

    app.controller("MainControl", ['$scope', 'NgTableParams', 'Upload', function($scope, NgTableParams, Upload) {
        $scope.csv = {
            content: null,
            header: null,
            headerVisible: true,
            separator: ',',
            separatorVisible: true,
            result: null,
            encoding: 'utf8',
            encodingVisible: true
        };
        $scope.zipfile = null;
        $scope.ngparam = new NgTableParams({}, { dataset: $scope.content });

        // upload later on form submit or something similar
        $scope.submit = function() {
            if ($scope.form.file.$valid && $scope.file) {
                $scope.upload($scope.file);
            }
        };

        // upload on file select or drop
        $scope.upload = function(file) {
            Upload.upload({
                url: 'http://localhost:5000/upload',
                data: {file: file},
                method: 'POST'
            }).then(function(resp) {
                $scope.message = resp.data;
            }, function(resp) {
                console.log('Error status: ' + resp.status);
            });
        };
    }]);

})();