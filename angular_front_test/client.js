
angular.module("myapp.client", [])

.factory("api", ["$http", function($http) {

	return {
		upload: function() {
			console.log('lololololol');
		}
	};
}])