angular.module("myapp", ['ngMaterial', 'ngCsvImport', 'myapp.directives', 'myapp.client', 'ngTable'])
 
.controller("MainControl", ['$scope', 'api', 'NgTableParams', function($scope, api, NgTableParams) {
    $scope.lol = "idontevenunderstandanything";
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

    // Test
    api.upload();
 }]);

// .config(function($mdThemingProvider) {
//   $mdThemingProvider.theme('default')
//     .primaryPalette('pink')
//     .accentPalette('orange');
// });

